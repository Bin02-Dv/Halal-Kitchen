from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dash/", views.dash, name="dash"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("products/", views.products, name="products"),
    path("add-product/", views.add_product, name="add-product"),
    
    # CART
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/save/", views.save_cart, name="save_cart"),
    path("cart/get/", views.get_cart, name="get_cart"),
]
