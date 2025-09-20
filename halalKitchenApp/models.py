from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class AuthModel(AbstractUser):
    
    full_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=200, blank=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=100, blank=True)
    
    username = models.CharField(max_length=50, blank=True, unique=True)

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []
    

class Product(models.Model):
    
    product_name = models.CharField(max_length=100, blank=True)
    product_price = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    product_description = models.TextField(max_length=200, blank=True)
    product_image = models.ImageField(upload_to='product-images/', blank=True)


class CartItem(models.Model):
    user = models.ForeignKey(AuthModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    full_name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
