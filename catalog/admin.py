from django.contrib import admin
from .models import Product, Category, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'brand', 'flavor', 'volume', 'price', 
        'small_wholesale_price', 'large_wholesale_price',
        'is_alcoholic', 'category'
    )
    list_filter = ('category', 'is_alcoholic')
    search_fields = ('brand', 'flavor')
    fieldsets = (
        (None, {
            'fields': ('brand', 'flavor', 'category')
        }),
        ('Характеристики', {
            'fields': ('volume', 'sugar_content', 'is_alcoholic', 'expiration_date')
        }),
        ('Цены', {
            'fields': (
                'price', 
                ('small_wholesale_price', 'small_wholesale_quantity'),
                ('large_wholesale_price', 'large_wholesale_quantity')
            )
        }),
    )

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    inlines = [OrderItemInline]
    actions = ['confirm_orders', 'ship_orders']

    def confirm_orders(self, request, queryset):
        queryset.filter(status='draft').update(status='confirmed')
    confirm_orders.short_description = "Подтвердить выбранные заказы"

    def ship_orders(self, request, queryset):
        queryset.filter(status='confirmed').update(status='shipped')
    ship_orders.short_description = "Отметить как отправленные"

# from django.contrib import admin
# from .models import Product, Category

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('brand', 'flavor', 'volume', 'sugar_content', 'is_alcoholic', 'category')
#     list_filter = ('category', 'is_alcoholic')
#     search_fields = ('brand', 'flavor')
