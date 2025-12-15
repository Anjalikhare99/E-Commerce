from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
import random
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == "POST":
        identifier = request.POST.get("phone_or_email", "").strip()
        otp = request.POST.get("otp", "").strip()
        role = request.GET.get("role", "C")

        if not identifier:
            return JsonResponse({"status": "error", "message": "Phone number or email required"}, status=400)

        # Check if identifier is email or phone
        is_email = "@" in identifier and "." in identifier  # simple email check

        try:
            if is_email:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(phone_number=identifier)
        except User.DoesNotExist:
            user = None

        if not otp:
            if user:
                return JsonResponse({"status": "error", "message": "User already registered, please login"}, status=400)
            
            generated_otp = random.randint(100000, 999999)

            if is_email:
                name_part = identifier.split("@")[0]
                user = User.objects.create(
                    email=identifier,
                    username=identifier,
                    name=name_part,
                    role=role,
                    password=make_password("temp1234"),
                    is_active=False
                )
            else:
                user = User.objects.create(
                    phone_number=identifier,
                    username=identifier,
                    name="Guest",
                    role=role,
                    password=make_password("temp1234"),
                    is_active=False
                )
            user.otp = generated_otp
            user.save()
            print(f"OTP sent to {identifier}: {generated_otp}")
            return JsonResponse({"status": "otp_sent", "message": "OTP sent successfully"})

        if user and str(user.otp) == otp:
            user.otp = None
            user.is_active = True
            user.password = make_password("default1234")
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return JsonResponse({"status": "success", "message": "Signup complete"})

        return JsonResponse({"status": "error", "message": "Invalid OTP"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)


def login_view(request):
    if request.method == "GET":
        return render(request, "index.html")
    
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
            print("Logged in user:", request.user)
            login(request, user)
            return JsonResponse({"status": "success", "message": "Login successful"})

        return JsonResponse({"status": "error", "message": "Invalid OTP"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)

def logout_view(request):
    logout(request)
    return redirect("/")

def index(request):
    return render(request, 'index.html')

def about_as(request):
    return render(request, 'about.html')

def contact_as(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

@login_required
def address(request):
    if request.method == 'GET':
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'address.html', {"addresses": addresses})
    
    if request.method == 'POST':
        name = request.POST.get('name')
        address_type = request.POST.get('address_type')
        pincode = request.POST.get('pincode')
        house_or_flat_number = request.POST.get('house_or_flat_number')
        colony_or_area = request.POST.get('colony_or_area')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        landmark = request.POST.get('landmark')

        errors = {}

        if not name:
            errors['name'] = "Name is required."
        if not address_type:
            errors['address_type'] = "Address type is required."
        if not pincode:
            errors['pincode'] = "Pincode is required."
        if not house_or_flat_number:
            errors['house_or_flat_number'] = "House/Flat number is required."
        if not city:
            errors['city'] = "City is required."
        if not state:
            errors['state'] = "State is required."
        if not country:
            errors['country'] = "Country is required."

        if errors:
            return render(request, 'address.html', {
                'errors': errors,
                'values': request.POST,
            })

        Address.objects.create(
            user=request.user,
            name=name,
            address_type=address_type,
            pincode=pincode,
            house_or_flat_number=house_or_flat_number,
            colony_or_area=colony_or_area,
            city=city,
            state=state,
            country=country,
            landmark=landmark
        )
        return redirect('address')  # Or wherever you want to go after saving

    return render(request, 'address.html')


def wishlist(request):
    return render(request, 'wishlist.html')

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def products(request):
    return render(request, 'products.html')