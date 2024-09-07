from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from .models import User, Customer, Vendor, Admin, UserProfile, UserAddress
from .serializers import LoginSerializer, UserSerializer, CustomerSerializer, VendorSerializer, AdminSerializer, UserProfileSerializer, UserAddressSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate, login

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

class CreateUserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        data = request.data

        email = data.get('email')
        phone_number = data.get('phone_number')

        if not email and not phone_number:
            return Response({'error': 'Either email or phone number must be provided.'}, status=status.HTTP_400_BAD_REQUEST)

        username = email if email else phone_number
        data['username'] = username

        serializer = UserRegistrationSerializer(data=data, context={'request': request})

        if email:
            if User.objects.filter(email=email).exists():
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        elif phone_number:
            if User.objects.filter(phone_number=phone_number).exists():
                return Response({'error': 'User with this phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            try:
                user = serializer.save()

                token, created = Token.objects.get_or_create(user=user)
                token_key = token.key

                response_data = serializer.data
                response_data['token'] = token_key
                return Response(response_data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                print(e)
                return Response({'error': 'Account details already exist.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in and return a success response
            login(request, user)
            return Response({'message': 'Login successful', 'token': user.auth_token.key})
        else:
            # Authentication failed; return an error response
            return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomerRegistrationSerializer
from django.db import transaction

class CustomerRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        data['user_type'] = 'customer'  # Add the user_type field
        serializer = CustomerRegistrationSerializer(data=data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()  # Save the instance
                token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'message': 'Customer registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
