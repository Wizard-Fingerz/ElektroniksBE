from django.db import models

from app.products.models import Product

class Promotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)