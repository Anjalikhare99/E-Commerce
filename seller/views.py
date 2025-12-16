import random
import string
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import *
from accounts.models import *

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

def category_list_view(request):
    categories = Category.objects.all()
    return render(request, "seller/category_list.html", {
        "categories": categories
    })

from django.http import JsonResponse

def category(request):
    errors = {}

    if request.method == "POST":
        category_name = request.POST.get("category_name", "").strip()
        description = request.POST.get("description", "").strip()
        image = request.FILES.get("image")

        if not category_name:
            errors["category_name"] = "Category name is required"

        if not image:
            errors["image"] = "Category image is required"

        if errors:
            return JsonResponse({"status": "error", "errors": errors})

        Category.objects.create(
            category_name=category_name,
            description=description,
            image=image,
            user=request.user
        )

        return JsonResponse({"status": "success"})

    return render(request, "seller/category_add.html")


def subcategory_list_view(request):
    subcategories = SubCategory.objects.select_related('category_name').all()
    return render(request, "seller/subcategory_list.html", {
        "subcategories": subcategories
    })

def subcategory(request):
    errors = {}

    if request.method == "POST":
        category_id = request.POST.get("category_id", "").strip()
        sub_category_name = request.POST.get("sub_category_name", "").strip()
        description = request.POST.get("description", "").strip()

        if not category_id:
            errors["category"] = "Category is required"

        if not sub_category_name:
            errors["sub_category_name"] = "Sub-category name is required"

        if errors:
            return JsonResponse({
                "status": "error",
                "errors": errors
            })

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "errors": {"category": "Invalid category"}
            })

        SubCategory.objects.create(
            category_name=category,
            subcategory_name=sub_category_name,
            description=description
        )

        return JsonResponse({
            "status": "success",
            "message": "Sub-category added successfully"
        })

    categories = Category.objects.all()

    return render(request, "seller/subcategory_add.html", {
        "categories": categories
    }) 

def parse_description(text):
    """
    Converts: 'price=5500, color=red, size=M'
    Into: {'price': 5500, 'color': 'red', 'size': 'M'}
    """
    data = {}

    pairs = text.split(",")

    for pair in pairs:
        if "=" in pair:
            key, value = pair.split("=", 1)
            key = key.strip()
            value = value.strip()

            # convert numbers automatically
            if value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass

            data[key] = value

    return data

def product_list_view(request):
    products = Product.objects.select_related('category', 'subcategory_name').all()
    return render(request, "seller/product_list.html", {
        "products": products
    })
def product(request):
    if request.method =="POST":
        category_id = request.POST.get("category_id", "").strip()
        subcategory_id = request.POST.get("sub_category_id", "").strip()
        product_name = request.POST.get("product_name", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "").strip()
        stock = request.POST.get("stock", "").strip()
        image = request.FILES.get("image")

        errors = {}

        if not category_id:
            errors["category"] = "Category is required"

        if not subcategory_id:
            errors["subcategory_name"] = "Sub-category is required"

        if not product_name:
            errors["product_name"] = "Product name is required"

        if not price:
            errors["price"] = "Price is required"

        if not stock:
            errors["stock"] = "Stock is required"

        if not image:
            errors["image"] = "Product image is required"

        if not description:
            errors["description"] = "Description is required"

        try:
            description_dict = parse_description(description)
        except Exception:
            errors["description"] = "Invalid description format"

        if "price" in description_dict and description_dict["price"] <= 0:
            errors["description"] = "Price must be greater than 0"

        if errors:
            return JsonResponse({"status": "error", "errors": errors})

        try:
            category = Category.objects.get(id=category_id)
            subcategory = SubCategory.objects.get(id=subcategory_id)
        except (Category.DoesNotExist, SubCategory.DoesNotExist):
            return JsonResponse({
                "status": "error",
                "errors": {"category": "Invalid category or sub-category"}
            })

        Product.objects.create(
            user=request.user,
            category=category,
            subcategory_name=subcategory,
            product_name=product_name,
            description=description_dict,
            price=price,
            stock=stock,
            image=image
        )

        return JsonResponse({"status": "success", "message": "Product added successfully"})
    return render(request, "seller/product_add.html", { "categories": Category.objects.all(),
        "subcategories": SubCategory.objects.all()})