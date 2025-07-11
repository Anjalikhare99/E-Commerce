from django.db import models
from accounts.models import User

class Seller(models.Model):
    BUSINESS_TYPE=[
        ("I", "Individual"),
        ("C", "Company"),
        ("P", "Partnership"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    display_name = models.CharField(max_length=100)
    store_name = models.CharField(max_length=255)
    store_description = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='sellers/profile_images/', blank=True, null=True)
    store_address = models.TextField()
    pincode = models.CharField(max_length=10)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE)
    gst_number = models.CharField(max_length=20)
    signature = models.ImageField(upload_to='sellers/signatures/')
    bank_account_number = models.CharField(max_length=30)
    ifsc_code = models.CharField(max_length=15)
    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.display_name} ({self.store_name})"