from django.shortcuts import render, redirect
from django.contrib import auth
from . import models
from django.http import JsonResponse

# Create your views here.

def logout(request):
    auth.logout(request)
    return redirect('/login/')


def index(request):
    current_user = request.user
    context = {
        "current_user": current_user
    }
    return render(request, "index.html", context)

def cart(request):
    current_user = request.user
    context = {
        "current_user": current_user
    }
    return render(request, "cart.html", context)

def checkout(request):
    current_user = request.user
    context = {
        "current_user": current_user
    }
    return render(request, "checkout.html", context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = models.AuthModel.objects.filter(email=email).first()
        
        if not user:
            return JsonResponse({
                "message": "Sorry we couldn't find any user with the Email specified!!",
                "success": False
            })
        elif not user.check_password(password):
            return JsonResponse({
                "message": "Sorry your password is incorrect!!",
                "success": False
            })
        
        else:
            auth.login(request, user)
            return JsonResponse({
                "message": "Login successfully...",
                "success": True
            })
    current_user = request.user
    context = {
        "current_user": current_user
    }
    return render(request, "login.html", context)

def products(request):
    current_user = request.user
    context = {
        "current_user": current_user
    }
    return render(request, "products.html", context)

def add_product(request):
    current_user = request.user
    if request.method == 'POST':
        product_name = request.POST.get("product_name")
        product_price = request.POST.get("product_price")
        product_description = request.POST.get("product_description")
        product_image = request.FILES.get("product_image")
        
        if not all([product_name, product_price, product_description, product_image]):
            return JsonResponse({
                "message": "Sorry All fields are required!!",
                "success": False
            })
        else:
            models.Product.objects.create(
                product_name=product_image, product_price=product_price, product_description=product_description,
                product_image=product_image
            )
            return JsonResponse({
                "message": "Product Added successfully...",
                "success": True
            })
    context = {
        "current_user": current_user
    }
    return render(request, "add-project.html", context)

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        state = request.POST.get("state")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        if not all([full_name, email, phone_number, state, password, confirm_password]):
            return JsonResponse({
                "message": "All fileds are required to processed!!",
                "success": False
            })
        
        elif models.AuthModel.objects.filter(email=email).exists():
            return JsonResponse({
                "message": f"Sorry the Email {email} already exist!!",
                "success": False
            })
        
        elif confirm_password != password:
            return JsonResponse({
                "message": "Sorry you password and confirm password missed match!!",
                "success": False
            })
        else:
            models.AuthModel.objects.create_superuser(
                full_name=full_name, email=email, phone_number=phone_number, state=state,
                password=password, username=email
            )
            return JsonResponse({
                "message": "Registration completed successfully...",
                "success": True
            })
    current_user = request.user
    context = {
        "current_user": current_user
    }
    return render(request, "register.html", context)