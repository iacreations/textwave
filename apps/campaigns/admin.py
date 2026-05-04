from django.contrib import admin
from .models import Campaign, CampaignRecipient

class CampaignRecipientInline(admin.TabularInline):
    model = CampaignRecipient
    extra = 0
    readonly_fields = ['sent_at', 'created_at']

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'status', 'total_recipients', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'user__username']
    inlines = [CampaignRecipientInline]

@admin.register(CampaignRecipient)
class CampaignRecipientAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'campaign', 'status', 'sent_at']
    list_filter = ['status']
    search_fields = ['phone_number', 'campaign__name']
