from django.contrib import admin

# Register your models here.
from .models import CategoryModel, ProductModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category_title', 'created_at']
    search_fields = ['category_title',]
    list_filter = ['created_at']
    ordering = ['created_at']

    @admin.register(ProductModel)
    class ProductAdmin(admin.ModelAdmin):
        list_display = ['product_title', 'product_price', 'product_created_at']
        search_fields = ['product_title']
        list_filter = ['product_created_at']
        ordering = ['product_title']

