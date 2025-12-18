from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('send_otp/', send_otp, name="send_otp"),
    path('verify_otp/', verify_otp, name="verify_otp"),
    path('become_a_seller/', seller_signup, name="seller"),
    path('signin/', seller_signin, name="signin"),
    path('category/', category, name="category"),
    path('categorys/', category_list_view, name='category_list'),
    path('subcategory/', subcategory, name="subcategory"),
    path('subcategories/', subcategory_list_view, name='subcategory_list'),
    path('product/', product, name="product_add"),
    path('products/', product_list_view, name='product_list'),
    path('product/<int:product_id>/', product_detail_view, name='product_detail'),
    path('product/<int:product_id>/edit/', product_edit_view, name='product_edit'),
]