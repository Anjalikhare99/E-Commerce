from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ["user", "store_name"]