from rest_framework import serializers
from .models import Order, OrderItem, OrderPayment, ShippingAddress
from account.serializers import UserSerializer
from app.products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'total_cost', 'status', 'order_items']

class OrderPaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = OrderPayment
        fields = ['id', 'order', 'payment_method', 'payment_date', 'amount']

class ShippingAddressSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = ShippingAddress
        fields = ['id', 'order', 'address', 'city', 'state', 'zip_code', 'country']