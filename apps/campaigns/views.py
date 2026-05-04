from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Campaign, CampaignRecipient
from .forms import CampaignForm
from .services import send_campaign
from apps.contacts.models import Contact, ContactGroup

@login_required
def campaign_list(request):
    campaigns = Campaign.objects.filter(user=request.user)
    paginator = Paginator(campaigns, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'campaigns/campaign_list.html', {'page_obj': page_obj})

@login_required
def campaign_create(request):
    form = CampaignForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        campaign = form.save(commit=False)
        campaign.user = request.user
        send_option = form.cleaned_data['send_option']
        if send_option == 'draft':
            campaign.status = 'draft'
        elif send_option == 'schedule':
            campaign.status = 'scheduled'
            scheduled_at = request.POST.get('scheduled_at')
            if scheduled_at:
                from django.utils.dateparse import parse_datetime
                campaign.scheduled_at = parse_datetime(scheduled_at)
        else:
            campaign.status = 'draft'
        campaign.save()
        recipient_type = form.cleaned_data['recipient_type']
        phones = set()
        if recipient_type == 'groups':
            for group in form.cleaned_data['groups']:
                for contact in Contact.objects.filter(group=group, user=request.user):
                    phones.add(contact.phone)
        else:
            raw = form.cleaned_data['manual_numbers']
            for p in raw.replace(',', '\n').split('\n'):
                p = p.strip()
                if p:
                    phones.add(p)
        for phone in phones:
            CampaignRecipient.objects.create(campaign=campaign, phone_number=phone)
        if send_option == 'now':
            if not phones:
                messages.error(request, 'No recipients found.')
                campaign.delete()
                return render(request, 'campaigns/campaign_form.html', {'form': form})
            balance = request.user.profile.sms_balance
            if balance < len(phones):
                messages.error(request, f'Insufficient SMS balance. You need {len(phones)} credits but have {balance}.')
                campaign.delete()
                return render(request, 'campaigns/campaign_form.html', {'form': form})
            success, failed = send_campaign(campaign)
            messages.success(request, f'Campaign sent! {success} delivered, {failed} failed.')
        elif send_option == 'schedule':
            messages.success(request, f'Campaign scheduled for {campaign.scheduled_at}.')
        else:
            messages.success(request, 'Campaign saved as draft.')
        return redirect('campaigns:campaign_list')
    return render(request, 'campaigns/campaign_form.html', {'form': form})

@login_required
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    recipients = campaign.recipients.all()
    paginator = Paginator(recipients, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    stats = {
        'total': campaign.total_recipients(),
        'sent': campaign.sent_count(),
        'delivered': campaign.delivered_count(),
        'failed': campaign.failed_count(),
        'pending': campaign.pending_count(),
    }
    return render(request, 'campaigns/campaign_detail.html', {'campaign': campaign, 'page_obj': page_obj, 'stats': stats})

@login_required
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    if request.method == 'POST':
        name = campaign.name
        campaign.delete()
        messages.success(request, f'Campaign "{name}" deleted.')
    return redirect('campaigns:campaign_list')

@login_required
def campaign_send(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, user=request.user)
    if request.method == 'POST' and campaign.status in ('draft', 'scheduled'):
        total = campaign.total_recipients()
        balance = request.user.profile.sms_balance
        if balance < total:
            messages.error(request, f'Insufficient balance. Need {total} credits, have {balance}.')
        else:
            success, failed = send_campaign(campaign)
            messages.success(request, f'Campaign sent! {success} delivered, {failed} failed.')
    return redirect('campaigns:campaign_detail', pk=pk)
