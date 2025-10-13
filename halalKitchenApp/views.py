from django.shortcuts import render, redirect
from django.contrib import auth
from . import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Sum

# Create your views here.

def logout(request):
    auth.logout(request)
    return redirect('/login/')

def about(request):
    current_user = request.user
    products = models.Product.objects.all()

    saved_carts = None
    if request.user.is_authenticated:
        saved_carts = models.CartItem.objects.filter(user=current_user)

    context = {
        "current_user": current_user,
        "products": products,
        "saved_carts": saved_carts
    }
    return render(request, "about.html", context)

@login_required(login_url='/login/')
def dash(request):
    current_user = request.user
    products = models.Product.objects.all()
    users = models.AuthModel.objects.all().exclude(is_superuser=True)
    total_order = models.OrderItem.objects.aggregate(total_price=Sum('price'))['total_price']

    saved_carts = None
    if request.user.is_authenticated:
        saved_carts = models.CartItem.objects.filter(user=current_user)

    context = {
        "current_user": current_user,
        "products": products,
        "saved_carts": saved_carts,
        "users": users,
        "total_order": total_order
    }
    return render(request, 'dashboard.html', context)


def index(request):
    current_user = request.user
    products = models.Product.objects.all()

    saved_carts = None
    if request.user.is_authenticated:
        saved_carts = models.CartItem.objects.filter(user=current_user)

    context = {
        "current_user": current_user,
        "products": products,
        "saved_carts": saved_carts, 
    }
    return render(request, "index.html", context)

def cart(request):
    current_user = request.user
    context = {
        "current_user": current_user
    }
    return render(request, "cart.html", context)

@csrf_exempt
def checkout(request):
    current_user = request.user
    products = models.Product.objects.all()
    saved_carts = None
    if request.user.is_authenticated:
        saved_carts = models.CartItem.objects.filter(user=current_user)
        
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        payment_method = request.POST.get("payment_method")
        cart = json.loads(request.POST.get("cart", "[]"))
        receipt = request.FILES.get("receipt")  # ✅ Handle file correctly
        
        # Create Order with Pending status
        order = models.Order.objects.create(
            full_name=full_name,
            address=address,
            phone=phone,
            payment_method=payment_method,
            status='Pending',
            receipt=receipt  # ✅ file saved to MEDIA_ROOT automatically
        )

        total = 0
        # Create Order Items
        for item in cart:
            product = models.Product.objects.get(id=item["product_id"])
            models.OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=product.product_price
            )
            total += product.product_price * item["quantity"]

        order.total = total
        order.save()

        if saved_carts:
            saved_carts.delete()

        return JsonResponse({"success": True, "order_id": order.id})

    context = {
        "current_user": current_user,
        "products": products,
        "saved_carts": saved_carts
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
    products = models.Product.objects.all()
    saved_carts = None
    if request.user.is_authenticated:
        saved_carts = models.CartItem.objects.filter(user=current_user)
    context = {
        "current_user": current_user,
        "products": products,
        "saved_carts": saved_carts
    }
    return render(request, "products.html", context)

def view_products_by_category(request, category):
    current_user = request.user
    products = models.Product.objects.filter(product_category=category)
    saved_carts = None
    if request.user.is_authenticated:
        saved_carts = models.CartItem.objects.filter(user=current_user)
    context = {
        "current_user": current_user,
        "products": products,
        "saved_carts": saved_carts
    }
    return render(request, "products.html", context)

def add_product(request):
    current_user = request.user
    if request.method == 'POST':
        product_name = request.POST.get("product_name")
        category = request.POST.get("category")
        product_price = request.POST.get("product_price")
        product_description = request.POST.get("product_description")
        product_image = request.FILES.get("product_image")
        
        if not all([product_name, product_price, product_description, product_image, category]):
            return JsonResponse({
                "message": "Sorry All fields are required!!",
                "success": False
            })
        else:
            models.Product.objects.create(
                product_name=product_name, product_category=category, product_price=product_price, product_description=product_description,
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
            models.AuthModel.objects.create_user(
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

@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id", 0)
        user = request.user

        try:
            
            product = models.Product.objects.get(id=product_id)
            cart_item, created = models.CartItem.objects.get_or_create(user=user, product=product)
        except models.Product.DoesNotExist:
            pass

        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({"message": "Added to cart", "quantity": cart_item.quantity})

@csrf_exempt
def save_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        request.session["cart"] = data.get("cart", [])
        return JsonResponse({"message": "Cart saved successfully"})
    
def get_cart(request):
    cart = request.session.get("cart", [])
    return JsonResponse({"cart": cart})

@csrf_exempt
def delete_product(request, product_id):
    if request.method == "DELETE":
        try:
            product = models.Product.objects.get(id=product_id)
            product.delete()
            return JsonResponse({"success": True, "message": "Product deleted"})
        except models.Product.DoesNotExist:
            return JsonResponse({"success": False, "message": "Product not found"}, status=404)
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def all_payments(request):
    current_user = request.user
    products = models.Product.objects.all()
    users = models.AuthModel.objects.all().exclude(is_superuser=True)
    orders = models.Order.objects.all().order_by('-id')
    total_order = models.OrderItem.objects.aggregate(total_price=Sum('price'))['total_price']

    saved_carts = None
    if request.user.is_authenticated:
        saved_carts = models.CartItem.objects.filter(user=current_user)

    context = {
        "current_user": current_user,
        "products": products,
        "saved_carts": saved_carts,
        "users": users,
        "total_order": total_order,
        "orders": orders,
    }
    return render(request, "all-payments.html", context)

def approve(request, id):
    order = models.Order.objects.filter(id=id).first()
    order.status = 'Completed'
    order.save()
    return redirect('/all-payments/')