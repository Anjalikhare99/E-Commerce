from django.urls import path, include
from accounts.views import *

urlpatterns = [
    path("", index, name="index"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    path('about/', about_as, name='about'),
    path('contact/', contact_as, name='contact'),
    path('address/', address, name='address'),
     path('category/', category_list_view, name='category_list'),
    path('category/add/', add_category_view, name='add_category'),
    path('oauth/', include('social_django.urls', namespace='social')),
]