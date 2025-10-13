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
    path("view_products_by_category/<str:category>", views.view_products_by_category, name="view_products_by_category"),
    path("all-payments/", views.all_payments, name="all-payments"),
    path("add-product/", views.add_product, name="add-product"),
    path("products/delete/<int:product_id>/", views.delete_product, name="delete_product"),
    
    # CART
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/save/", views.save_cart, name="save_cart"),
    path("cart/get/", views.get_cart, name="get_cart"),
    
    path("approve/<int:id>", views.approve, name="approve")
]
