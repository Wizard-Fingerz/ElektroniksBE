from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    user_type = models.CharField(max_length=10, choices=[
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin')
    ])

    def __str__(self):
        return self.username

# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    profile_picture = models.ImageField(upload_to='customers/', blank=True)

    def __str__(self):
        return f"Customer {self.user.username}"

# Vendor Model
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    company_name = models.CharField(max_length=255)
    company_description = models.TextField()
    company_address = models.TextField()

    def __str__(self):
        return f"Vendor {self.user.username}"

# Admin Model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')

    def __str__(self):
        return f"Admin {self.user.username}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=255)