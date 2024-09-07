from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import User, Customer, Vendor, Admin, UserProfile, UserAddress

# Register your models here.

class UserAdmin(ImportExportModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'address', 'user_type')
    list_filter = ('user_type',)
    search_fields = ('username', 'email', 'phone_number')

class CustomerAdmin(ImportExportModelAdmin):
    list_display = ('user', 'profile_picture')
    search_fields = ('user__username',)

class VendorAdmin(ImportExportModelAdmin):
    list_display = ('user', 'company_name', 'company_description', 'company_address')
    search_fields = ('user__username', 'company_name')

class AdminAdmin(ImportExportModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username',)

class UserAddressAdmin(ImportExportModelAdmin):
    list_display = ('user', 'address', 'city', 'state', 'zip_code', 'country')
    search_fields = ('user__username',)

admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAddress, UserAddressAdmin)