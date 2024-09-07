# admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, Category, ProductVariation, ProductReview, ProductImage
from .resources import ProductResource, CategoryResource, ProductVariationResource, ProductReviewResource, ProductImageResource

class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('title', 'price', 'category', 'vendor')
    search_fields = ('title', 'description')

class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class ProductVariationAdmin(ImportExportModelAdmin):
    resource_class = ProductVariationResource
    list_display = ('product', 'variation_type', 'variation_value')
    search_fields = ('product__title', 'variation_type', 'variation_value')

class ProductReviewAdmin(ImportExportModelAdmin):
    resource_class = ProductReviewResource
    list_display = ('product', 'user', 'rating', 'review')
    search_fields = ('product__title', 'user__username', 'review')

class ProductImageAdmin(ImportExportModelAdmin):
    resource_class = ProductImageResource
    list_display = ('product', 'image')
    search_fields = ('product__title',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(ProductImage, ProductImageAdmin)

admin.site.site_header = "Electroniks Administrator"