from django.urls import path, include
from accounts.views import *

urlpatterns = [
    path("", index, name="index"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
]