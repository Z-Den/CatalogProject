from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('brand', 'flavor', 'volume', 'sugar_content', 'is_alcoholic', 'category')
    list_filter = ('category', 'is_alcoholic')
    search_fields = ('brand', 'flavor')
