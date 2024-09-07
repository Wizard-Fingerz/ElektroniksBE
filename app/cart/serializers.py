# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem, CartCoupon
from app.products.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at']

class CartItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'price']

class DetailCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'price']


class CartCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartCoupon
        fields = ['id', 'cart', 'coupon_code', 'discount_amount', 'is_active']