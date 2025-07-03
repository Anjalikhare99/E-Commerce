from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
import random

@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        otp = request.POST.get("otp", "").strip()
        role = request.GET.get("role", "C")

        if not phone:
            return JsonResponse({"status": "error", "message": "Phone number required"}, status=400)

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            user = None

        if not otp:
            generated_otp = random.randint(100000, 999999)
            if not user:
                user = User.objects.create(
                    phone_number=phone,
                    username=phone,
                    name="Guest",
                    role=role,
                    gender="O",
                    password=make_password("temp1234"),
                    is_active=False
                )
            user.otp = generated_otp
            user.save()
            print(f"OTP sent to {phone}: {generated_otp}")
            return JsonResponse({"status": "otp_sent", "message": "OTP sent successfully"})

        if user and str(user.otp) == otp:
            user.otp = None
            user.is_active = True
            user.password = make_password("default1234")
            user.save()
            return JsonResponse({"status": "success", "message": "Signup complete"})

        return JsonResponse({"status": "error", "message": "Invalid OTP"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier", "").strip()
        otp = request.POST.get("otp", "").strip()

        if "@" in identifier:
            user = User.objects.filter(email=identifier).first()
        else:
            user = User.objects.filter(phone_number=identifier).first()

        if not user:
            return JsonResponse({"status": "error", "message": "User not found"}, status=404)

        if not otp:
            user.otp = random.randint(100000, 999999)
            user.save()
            print(f"OTP sent to {identifier}: {user.otp}")
            return JsonResponse({"status": "otp_sent", "message": "OTP sent to your number/email"})

        if str(user.otp) == otp:
            user.otp = None
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return JsonResponse({"status": "success", "message": "Login successful"})

        return JsonResponse({"status": "error", "message": "Invalid OTP"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)

def logout_view(request):
    logout(request)
    return redirect("/")

def index(request):
    return render(request, 'index.html')