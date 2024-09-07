from django.db import models

from app.products.models import Product

class ShippingOption(models.Model):
    shipping_option = models.CharField(max_length=20)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class ShippingRate(models.Model):
    shipping_option = models.ForeignKey(ShippingOption, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2)