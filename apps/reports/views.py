import csv
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from apps.campaigns.models import CampaignRecipient, Campaign

@login_required
def report_list(request):
    status_filter = request.GET.get('status', '')
    campaign_filter = request.GET.get('campaign', '')
    recipients = CampaignRecipient.objects.filter(campaign__user=request.user).select_related('campaign')
    if status_filter:
        recipients = recipients.filter(status=status_filter)
    if campaign_filter:
        recipients = recipients.filter(campaign_id=campaign_filter)
    campaigns = Campaign.objects.filter(user=request.user)
    paginator = Paginator(recipients, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    stats = {
        'total': CampaignRecipient.objects.filter(campaign__user=request.user).count(),
        'sent': CampaignRecipient.objects.filter(campaign__user=request.user, status='sent').count(),
        'delivered': CampaignRecipient.objects.filter(campaign__user=request.user, status='delivered').count(),
        'failed': CampaignRecipient.objects.filter(campaign__user=request.user, status='failed').count(),
        'pending': CampaignRecipient.objects.filter(campaign__user=request.user, status='pending').count(),
    }
    return render(request, 'reports/report_list.html', {
        'page_obj': page_obj, 'stats': stats, 'campaigns': campaigns,
        'status_filter': status_filter, 'campaign_filter': campaign_filter,
    })

@login_required
def export_csv(request):
    recipients = CampaignRecipient.objects.filter(campaign__user=request.user).select_related('campaign')
    status_filter = request.GET.get('status', '')
    if status_filter:
        recipients = recipients.filter(status=status_filter)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="delivery_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Campaign', 'Phone Number', 'Status', 'Message ID', 'Sent At', 'Created At'])
    for r in recipients:
        writer.writerow([r.campaign.name, r.phone_number, r.status, r.message_id, r.sent_at, r.created_at])
    return response
