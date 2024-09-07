from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.cart.models import CartItem
from app.payment.bank_transfer import generate_paystack_bank_transfer_payment_link
from app.payment.flutterwave import generate_flutterwave_payment_link
from app.payment.paypal import generate_paypal_payment_link
from app.products.models import Product

from .models import Order, OrderItem, OrderPayment, ShippingAddress
from .serializers import OrderSerializer, OrderItemSerializer, OrderPaymentSerializer, ShippingAddressSerializer

class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        user = request.user
        order = Order.objects.create(user=user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

class OrderItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def create(self, request):
        order_id = request.data.get('order_id')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        order = Order.objects.get(id=order_id)
        product = Product.objects.get(id=product_id)

        order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)
        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderPaymentViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer

    def create(self, request):
        order_id = request.data.get('order_id')
        payment_method = request.data.get('payment_method')
        amount = request.data.get('amount')

        order = Order.objects.get(id=order_id)
        payment = OrderPayment.objects.create(order=order, payment_method=payment_method, amount=amount)
        serializer = OrderPaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ShippingAddressViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer

    def create(self, request):
        order_id = request.data.get('order_id')
        address = request.data.get('address')
        city = request.data.get('city')
        state = request.data.get('state')
        zip_code = request.data.get('zip_code')
        country = request.data.get('country')

        order = Order.objects.get(id=order_id)
        shipping_address = ShippingAddress.objects.create(order=order, address=address, city=city, state=state, zip_code=zip_code, country=country)
        serializer = ShippingAddressSerializer(shipping_address)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CheckoutViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        print(request.data)
        # Get the shipping address and payment method from the request data
        shipping_address = request.data.get('shipping_address')
        payment_method = request.data.get('payment_method')
        total = request.data.get('total')  # Get the total amount from the request data

        # Get the order items from the request data
        order_items = request.data.get('order_items')

        # Create a new order
        order = Order.objects.create(user=request.user, status='pending', total_cost=total)  # Update the total_cost field of the Order object

        # Add the order items to the order
        for item in order_items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)

            # Remove the item from the cart
            cart_item = CartItem.objects.filter(cart__user=request.user, product=product).first()
            if cart_item:
                cart_item.delete()

        # Create a new shipping address
        shipping_address_obj = ShippingAddress.objects.create(
            order=order,
            address=shipping_address.get('streetAddress'),
            city=shipping_address.get('city'),
            state=shipping_address.get('state'),
            zip_code=shipping_address.get('zipCode'),
            country=shipping_address.get('country')
        )

        # Create a new payment
        payment = OrderPayment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=total  # Use the total amount from the request data
        )

        # Generate a payment link based on the payment method
        if payment_method == 'paypal':
            payment_link = generate_paypal_payment_link(payment, total)
        elif payment_method == 'flutterwave':
            payment_link = generate_flutterwave_payment_link(payment, total)
        elif payment_method == 'bank_transfer':
            payment_link = generate_paystack_bank_transfer_payment_link(payment, total)
        else:
            return Response({'message': 'Invalid payment method'}, status=status.HTTP_400_BAD_REQUEST)

        # Send the payment link as a response
        return Response({'payment_link': payment_link}, status=status.HTTP_200_OK)