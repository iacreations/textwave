from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'company', 'sms_balance', 'sender_id', 'created_at']
    search_fields = ['user__username', 'user__email', 'company', 'phone']
    list_filter = ['created_at']
    readonly_fields = ['api_key', 'created_at', 'updated_at']
