from rest_framework import serializers

from account.serializers import VendorSerializer
from .models import Product, Category, ProductVariation, ProductReview, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'image', 'category', 'vendor', 'created_at', 'updated_at', 'stock']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['id', 'product', 'variation_type', 'variation_value']

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'user', 'rating', 'review', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']

class DetailedProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    vendor = VendorSerializer()
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'image', 'category', 'vendor', 'created_at', 'updated_at', 'stock']
