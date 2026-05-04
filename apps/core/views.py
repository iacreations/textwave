from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.campaigns.models import Campaign, CampaignRecipient
from apps.contacts.models import Contact, ContactGroup
from apps.billing.models import Transaction

@login_required
def dashboard(request):
    user = request.user
    total_sent = CampaignRecipient.objects.filter(campaign__user=user).exclude(status='pending').count()
    delivered = CampaignRecipient.objects.filter(campaign__user=user, status='delivered').count()
    failed = CampaignRecipient.objects.filter(campaign__user=user, status='failed').count()
    balance = user.profile.sms_balance
    recent_campaigns = Campaign.objects.filter(user=user)[:5]
    contact_count = Contact.objects.filter(user=user).count()
    return render(request, 'core/dashboard.html', {
        'total_sent': total_sent, 'delivered': delivered, 'failed': failed,
        'balance': balance, 'recent_campaigns': recent_campaigns, 'contact_count': contact_count,
    })

@login_required
def settings_view(request):
    profile = request.user.profile
    return render(request, 'core/settings.html', {'profile': profile})

@login_required
def quick_send(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        sender_id = request.user.profile.sender_id or 'TextWave'
        if not phone or not message:
            messages.error(request, 'Phone number and message are required.')
            return redirect('core:dashboard')
        balance = request.user.profile.sms_balance
        if balance < 1:
            messages.error(request, 'Insufficient SMS balance.')
            return redirect('core:dashboard')
        from apps.campaigns.models import Campaign, CampaignRecipient
        from apps.campaigns.services import send_campaign
        campaign = Campaign.objects.create(
            name=f'Quick SMS to {phone}', message=message, sender_id=sender_id,
            user=request.user, status='draft'
        )
        CampaignRecipient.objects.create(campaign=campaign, phone_number=phone)
        success, failed = send_campaign(campaign)
        if success:
            messages.success(request, f'SMS sent successfully to {phone}!')
        else:
            messages.error(request, 'Failed to send SMS.')
    return redirect('core:dashboard')
