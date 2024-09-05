from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Ride
from .models import Payment



@admin.register(Ride)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_location', 'destination', 'ride_type', 'price', 'created_at')
    list_filter = ('ride_type', 'created_at')
    search_fields = ('user__username', 'current_location', )

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Display these fields in the admin list view
    list_display = ['username', 'email', 'is_staff', 'is_active']
    # Use the email field as a filter
    search_fields = ('username',)
    ordering = ('username',) 

admin.site.register(CustomUser, CustomUserAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ride', 'mpesa_code', 'amount', 'payment_date')
    search_fields = ('user_username', 'mpesa_code', 'ride_id')
    list_filter = ('payment_date', 'ride')
    ordering = ('-payment_date',)

admin.site.register(Payment, PaymentAdmin)