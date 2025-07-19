from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('send_otp/', send_otp, name="send_otp"),
    path('verify_otp/', verify_otp, name="verify_otp"),
    path('become_a_seller/', seller_signup, name="seller"),
    path('signin/', seller_signin, name="signin"),
    path('category/', category, name="category"),
]