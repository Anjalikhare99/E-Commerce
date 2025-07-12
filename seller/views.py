import random
import string
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "seller/index.html")

def generate_otp():
    return str(random.randint(100000, 999999))

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "status": "error",
                "message": "Email already registered"
            })

        if User.objects.filter(phone_number=phone).exists():
            return JsonResponse({"status": "error", "message": "Phone number already registered."})
        
        otp = generate_otp()

        user, created = User.objects.get_or_create(phone_number=phone, email=email,)
        user.otp = otp
        user.save()

        print("OTP for", phone, "is", otp)

        return JsonResponse({"status": "sent"})
    return JsonResponse({"status": "error"})

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        entered_otp = request.POST.get("otp")

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"})
        
        if str(user.otp) == str(entered_otp):
            return JsonResponse({"status": "success", "clear_otp_fields": True})
        else:
            return JsonResponse({"status": "error", "message": "Invalid OTP"})

def generate_password(length=10):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choices(characters, k=length))


def seller_signup(request):
    if request.method == "POST":
        phone = request.POST.get("phone")

        user, created = User.objects.get_or_create(phone_number=phone)

        if not created and user.role == "S":
            messages.error(request, "You are already registered as a seller.")
            return redirect("signin")
        
        if created:
            user.role = "S"
            password = generate_password()
            user.set_password(password)
            user.save()
            print("Password for new seller:", password)
        elif user.role != "S":
            user.role = "S"
            user.save()

        display_name = request.POST.get("display_name")
        store_name = request.POST.get("store_name")
        store_description = request.POST.get("store_description")
        profile_image = request.FILES.get("profile_image")
        store_address = request.POST.get("store_address")
        pincode = request.POST.get("pincode")
        business_type = request.POST.get("business_type")
        gst_number = request.POST.get("gst_number")
        signature = request.FILES.get("signature")
        bank_account_number = request.POST.get("bank_account_number")
        ifsc_code = request.POST.get("ifsc_code")
        account_holder_name = request.POST.get("account_holder_name")
        bank_name = request.POST.get("bank_name")

        Seller.objects.create(
            user=user,
            display_name=display_name,
            store_name=store_name,
            store_description=store_description,
            profile_image=profile_image,
            store_address=store_address,
            pincode=pincode,
            business_type=business_type,
            gst_number=gst_number,
            signature=signature,
            bank_account_number=bank_account_number,
            ifsc_code=ifsc_code,
            account_holder_name=account_holder_name,
            bank_name=bank_name,
        )

        messages.success(request, "Seller registered successfully.")
        return redirect("index")

    return render(request, "seller/sign-up.html")

def seller_signin(request):
    return render(request, "seller/sign-in.html")