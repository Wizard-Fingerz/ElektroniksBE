# cart/views.py
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import Cart, CartItem, CartCoupon
from .serializers import CartSerializer, CartItemSerializer, CartCouponSerializer, DetailCartItemSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CartViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = CartItem.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'get']:
            return DetailCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def create(self, request):
        print("Request data:", request.data)
        user = request.user
        print("User:", user)
        if not Cart.objects.filter(user=user).exists():
            cart = Cart.objects.create(user=user)
            print("Cart created:", cart)
        else:
            cart = Cart.objects.get(user=user)
            print("Cart retrieved:", cart)

        serializer = CartSerializer(cart)

        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        price = request.data.get('price')  # Get the price from the request data

        print("Product ID:", product_id)
        print("Quantity:", quantity)
        print("Price:", price)

        # Check if product_id and quantity are provided
        if not product_id or not quantity:
            return Response({'error': 'Product ID and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the product is already in the cart
        product_in_cart = CartItem.objects.filter(cart=cart, product_id=product_id).exists()

        if product_in_cart:
            # If the product is already in the cart, update the quantity
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.quantity += int(quantity)
            cart_item.save()
            print("Cart item updated:", cart_item)
        else:
            # If the product is not in the cart, create a new cart item
            cart_item = CartItem.objects.create(cart=cart, product_id=product_id, quantity=quantity, price=price)  # Pass the price to the CartItem instance
            print("Cart item created:", cart_item)

        # Serialize the cart item and return it in the response
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartCouponViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = CartCoupon.objects.all()
    serializer_class = CartCouponSerializer

    def get_queryset(self):
        return CartCoupon.objects.filter(cart__user=self.request.user)