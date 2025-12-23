from django.urls import path, include
from accounts.views import *
app_name = 'accounts'
urlpatterns = [
    path("", index, name="index"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    path('about/', about_as, name='about'),
    path('contact/', contact_as, name='contact'),
    path('address/', address, name='address'),
    path('faq/', faq, name='faq'),
    path('wishlist/', wishlist, name='wishlist'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('products/', products, name='products'),
    path('product/', product_detail, name='product_detail'),
    path('oauth/', include('social_django.urls', namespace='social')),
]