import uuid
from django.utils import timezone

class SMSGatewayService:
    def send_sms(self, phone, message, sender_id):
        return {"status": "delivered", "message_id": f"mock_{uuid.uuid4().hex[:8]}"}

    def send_bulk(self, recipients, message, sender_id):
        results = []
        for phone in recipients:
            result = self.send_sms(phone, message, sender_id)
            results.append({'phone': phone, 'status': result['status'], 'message_id': result['message_id']})
        return results


def send_campaign(campaign):
    from .models import CampaignRecipient
    service = SMSGatewayService()
    campaign.status = 'sending'
    campaign.save()
    recipients = campaign.recipients.filter(status='pending')
    success = 0
    failed = 0
    for recipient in recipients:
        try:
            result = service.send_sms(recipient.phone_number, campaign.message, campaign.sender_id)
            recipient.status = result['status']
            recipient.message_id = result['message_id']
            recipient.sent_at = timezone.now()
            recipient.save()
            if result['status'] in ('sent', 'delivered'):
                success += 1
            else:
                failed += 1
        except Exception:
            recipient.status = 'failed'
            recipient.save()
            failed += 1
    campaign.status = 'sent'
    campaign.save()
    total_sent = success
    if total_sent > 0 and hasattr(campaign.user, 'profile'):
        profile = campaign.user.profile
        profile.sms_balance = max(0, profile.sms_balance - total_sent)
        profile.save()
        from apps.billing.models import Transaction
        Transaction.objects.create(
            user=campaign.user, amount=0, credits=-total_sent,
            transaction_type='deduction', status='completed',
            description=f'SMS campaign: {campaign.name}'
        )
    return success, failed
