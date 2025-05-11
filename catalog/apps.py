from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CatalogConfig(AppConfig):
    name = 'catalog'

    def ready(self):
        # Используем локальный импорт
        from django.db import connection

        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        def safe_create_roles(sender, **kwargs):
            # Проверка, инициализирована ли таблица auth_user
            if 'auth_user' not in connection.introspection.table_names():
                return  # Таблиц ещё нет — выходим

            

            groups_data = {
                'Товаровед': {
                    'product': ['add', 'change', 'view', 'edit_product'],
                    'category': ['add', 'change', 'view'],
                },
                'Менеджер': {
                    'order': ['add', 'change', 'view', 'manage_order'],
                    'cart': ['add', 'change', 'view'],
                },
                'Гость': {
                    'product': ['view'],
                    'category': ['view'],
                }
            }

            for group_name, permissions in groups_data.items():
                group, _ = Group.objects.get_or_create(name=group_name)
                for model_name, actions in permissions.items():
                    try:
                        ct = ContentType.objects.get(app_label='catalog', model=model_name)
                        for action in actions:
                            codename = f'{action}_{model_name}'
                            try:
                                perm = Permission.objects.get(content_type=ct, codename=codename)
                                group.permissions.add(perm)
                            except Permission.DoesNotExist:
                                print(f"Permission {codename} not found")
                    except ContentType.DoesNotExist:
                        print(f"Model {model_name} not found")

        post_migrate.connect(safe_create_roles, sender=self)


# from django.apps import AppConfig
# from django.db.models.signals import post_migrate


# class CatalogConfig(AppConfig):
#     name = 'catalog'

#     def ready(self):
#         post_migrate.connect(create_roles, sender=self)

# def create_roles(sender, **kwargs):
#     from django.contrib.auth.models import Group, Permission
#     from django.contrib.contenttypes.models import ContentType
#     groups_data = {
#         'Товаровед': {
#             'product': ['add', 'change', 'view', 'edit_product'],
#             'category': ['add', 'change', 'view'],
#         },
#         'Менеджер': {
#             'order': ['add', 'change', 'view', 'manage_order'],
#             'cart': ['add', 'change', 'view'],
#         },
#         'Гость': {
#             'product': ['view'],
#             'category': ['view'],
#         }
#     }

#     for group_name, permissions in groups_data.items():
#         group, created = Group.objects.get_or_create(name=group_name)
#         for model_name, actions in permissions.items():
#             ct = ContentType.objects.get(app_label='catalog', model=model_name)
#             for action in actions:
#                 codename = f'{action}_{model_name}' if '_' in action else f'{action}_{model_name}'
#                 try:
#                     perm = Permission.objects.get(content_type=ct, codename=codename)
#                     group.permissions.add(perm)
#                 except Permission.DoesNotExist:
#                     print(f"Permission {codename} not found")

# ..........................................


# from django.apps import AppConfig


# class CatalogConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'catalog'
