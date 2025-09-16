from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class AuthModel(AbstractUser):
    
    full_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=200, blank=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=50, blank=True)
    
    username = models.CharField(max_length=50, blank=True, unique=True)

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []
    

class Product(models.Model):
    
    product_name = models.CharField(max_length=100, blank=True)
    product_price = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    product_description = models.TextField(max_length=200, blank=True)
    product_image = models.ImageField(upload_to='product-images/', blank=True)