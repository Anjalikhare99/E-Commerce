from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDER_TYPE_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    ROLE_CHOICE = [
        ("A", "Admin"),
        ("S", "Seller"),
        ("C", "Customer"),
    ]

    name = models.CharField(max_length=255)
    phone_number = models.CharField(unique=True, max_length=17, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_TYPE_CHOICES, null=True, blank=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICE)
    image = models.ImageField(upload_to="profile image/", null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'name', 'email']

    def __str__(self):
        return self.phone_number or self.email or "Unknown User"
    
# class Category(models.Model):
#     category_name = models.CharField(max_length=100)
#     description = models.TextField(max_length=150)
#     created_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.category_name
    
# class SubCategory(models.Model):
#     category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
#     subcategory_name = models.CharField(max_length=100)
#     description = models.TextField(max_length=150)
#     created_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.subcategory_name
    

    
