from rest_framework import serializers
from .models import User, Customer, Vendor, Admin, UserProfile, UserAddress
from django.contrib.auth import authenticate, login

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'address', 'user_type']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'profile_picture']

class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'user', 'company_name', 'company_description', 'company_address']

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Admin
        fields = ['id', 'user']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number', 'address']

class UserAddressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserAddress
        fields = ['id', 'user', 'address', 'city', 'state', 'zip_code', 'country']


class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)  # Make phone_number optional
    email = serializers.EmailField(required=False, allow_blank=True)  # Make email optional
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'username', 'password']

    def validate(self, validated_data):
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')

        if not email and not phone_number:
            raise serializers.ValidationError("Enter an email or a phone number.")

        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')
        username = email if email else phone_number  # Set username to email or phone_number

        # Debugging statement: Print the email and phone number
        print(f"Creating user with Email: {email}, Phone Number: {phone_number}")

        # Create and save the User instance
        user = User.objects.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=validated_data.get('password'),
        )

        return user

from rest_framework import serializers
from .models import Customer, User

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'profile_picture']

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password', 'user_type']
    
    def create(self, validated_data):
        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', ''),
            user_type='customer'  # Set user_type to customer
        )
        user.set_password(validated_data['password'])
        user.save()

        # Create Customer profile
        Customer.objects.create(user=user)

        return user

from rest_framework import serializers
from .models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid login credentials.")

        return data