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