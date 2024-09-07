# resources.py
from import_export import resources
from .models import Product, Category, ProductVariation, ProductReview, ProductImage

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'image', 'category', 'vendor', 'created_at', 'updated_at')

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class ProductVariationResource(resources.ModelResource):
    class Meta:
        model = ProductVariation
        fields = ('id', 'product', 'variation_type', 'variation_value')

class ProductReviewResource(resources.ModelResource):
    class Meta:
        model = ProductReview
        fields = ('id', 'product', 'user', 'rating', 'review', 'created_at')

class ProductImageResource(resources.ModelResource):
    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'image')