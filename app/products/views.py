
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from .models import Product, Category, ProductVariation, ProductReview, ProductImage
from .serializers import DetailedProductSerializer, ProductSerializer, CategorySerializer, ProductVariationSerializer, ProductReviewSerializer, ProductImageSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ProductSerializer
        return DetailedProductSerializer
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductVariationViewSet(viewsets.ModelViewSet):
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationSerializer

class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can create reviews

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        request.data['user'] = request.user.id

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer