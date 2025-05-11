from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создаёт группы пользователей и назначает права'

    def handle(self, *args, **kwargs):
        # Список групп
        groups = {
            'Товаровед': ['add_product', 'change_product', 'delete_product'],
            'Менеджер': [],  # Пока без прав, добавим позже
            'Гость': [],     # Только просмотр
        }

        for group_name, perm_codenames in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if perm_codenames:
                permissions = Permission.objects.filter(codename__in=perm_codenames)
                group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана или обновлена.'))