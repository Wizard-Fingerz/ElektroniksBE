from django.urls import path, include
from rest_framework import routers
from .views import CustomerLoginView, CustomerRegistrationView, UserViewSet, CustomerViewSet, VendorViewSet, AdminViewSet, UserProfileViewSet, UserAddressViewSet, CreateUserViewSet, LoginViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'admins', AdminViewSet)
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'useraddresses', UserAddressViewSet)
router.register(r'createuser', CreateUserViewSet, basename='createuser')
router.register(r'login', LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls)),
    path('customer/login/', CustomerLoginView.as_view(), name='login'),
    path('customer/register/', CustomerRegistrationView.as_view(), name='customer_register'),

]