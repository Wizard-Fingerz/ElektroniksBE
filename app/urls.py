from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'product-variations', views.ProductVariationViewSet)
router.register(r'product-reviews', views.ProductReviewViewSet)
router.register(r'product-images', views.ProductImageViewSet)
router.register(r'carts', views.CartViewSet, basename='cart')
router.register(r'cart-items', views.CartItemViewSet, basename='cart-item')
router.register(r'cart-coupons', views.CartCouponViewSet, basename='cart-coupon')
router.register(r'orders', views.OrderViewSet, basename='orders')
router.register(r'order-items', views.OrderItemViewSet, basename='order-items')
router.register(r'order-payments', views.OrderPaymentViewSet, basename='order-payments')
router.register(r'shipping-addresses', views.ShippingAddressViewSet, basename='shipping-addresses')
router.register(r'checkout', views.CheckoutViewSet, basename='checkout')

urlpatterns = [
    path('', include(router.urls)),
]