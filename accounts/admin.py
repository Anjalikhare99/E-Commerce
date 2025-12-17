from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Address)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ('category_name', 'user', 'created_at', 'update_at')
    search_fields = ('category_name', 'user__username')
    list_filter = ('created_at',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory_name', 'category_name', 'created_at', 'update_at')
    search_fields = ('subcategory_name', 'category_name__category_name')
    list_filter = ('created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'subcategory_name', 'price', 'stock', 'user', 'created_at', 'update_at')
    search_fields = ('product_name', 'category__category_name', 'subcategory_name__subcategory_name', 'user__username')
    list_filter = ('created_at',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'created_at', 'update_at')
    search_fields = ('product__product_name',)
    list_filter = ('created_at',)