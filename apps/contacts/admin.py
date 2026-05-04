from django.contrib import admin
from .models import Contact, ContactGroup

@admin.register(ContactGroup)
class ContactGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'contact_count', 'created_at']
    search_fields = ['name', 'user__username']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'group', 'user', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['group', 'created_at']
