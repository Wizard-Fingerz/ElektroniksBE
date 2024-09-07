from django.db import models

from account.models import User
from app.products.models import Product
# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

# Cart Item Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} x {self.quantity} in Cart {self.cart.id}"

# Cart Coupon Model
class CartCoupon(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    coupon_code = models.CharField(max_length=20)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Coupon {self.coupon_code} for Cart {self.cart.id}"