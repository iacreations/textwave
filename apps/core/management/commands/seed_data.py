from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile
from apps.contacts.models import Contact, ContactGroup
from apps.campaigns.models import Campaign, CampaignRecipient
from apps.billing.models import Transaction

class Command(BaseCommand):
    help = 'Seed database with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@textwave.com', 'admin123')
            admin.first_name = 'Admin'
            admin.last_name = 'User'
            admin.save()
            admin.profile.sms_balance = 10000
            admin.profile.company = 'TextWave Inc'
            admin.profile.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (admin/admin123)'))

        if not User.objects.filter(username='demo').exists():
            demo = User.objects.create_user('demo', 'demo@textwave.com', 'demo123')
            demo.first_name = 'Demo'
            demo.last_name = 'User'
            demo.save()
            demo.profile.sms_balance = 500
            demo.profile.company = 'Demo Company'
            demo.profile.save()
            self.stdout.write(self.style.SUCCESS('Created demo user (demo/demo123)'))
        else:
            demo = User.objects.get(username='demo')

        group1, _ = ContactGroup.objects.get_or_create(name='Customers', user=demo, defaults={'description': 'Regular customers'})
        group2, _ = ContactGroup.objects.get_or_create(name='VIP', user=demo, defaults={'description': 'VIP clients'})

        contacts_data = [
            ('Alice Johnson', '+1234567890', 'alice@example.com', group1),
            ('Bob Smith', '+1234567891', 'bob@example.com', group1),
            ('Carol Davis', '+1234567892', 'carol@example.com', group2),
            ('David Wilson', '+1234567893', 'david@example.com', group1),
            ('Eve Brown', '+1234567894', 'eve@example.com', group2),
            ('Frank Miller', '+1234567895', 'frank@example.com', group1),
            ('Grace Lee', '+1234567896', 'grace@example.com', group1),
            ('Henry Taylor', '+1234567897', 'henry@example.com', group2),
            ('Iris Anderson', '+1234567898', 'iris@example.com', group1),
            ('Jack Thomas', '+1234567899', 'jack@example.com', group2),
        ]
        for name, phone, email, group in contacts_data:
            Contact.objects.get_or_create(phone=phone, user=demo, defaults={'name': name, 'email': email, 'group': group})

        if Campaign.objects.filter(user=demo).count() < 2:
            c1 = Campaign.objects.create(
                name='Welcome Campaign',
                message='Welcome to our service! Enjoy 10% off your next purchase with code WELCOME10.',
                sender_id='TextWave', status='sent', user=demo
            )
            for contact in Contact.objects.filter(user=demo, group=group1):
                CampaignRecipient.objects.create(campaign=c1, phone_number=contact.phone, status='delivered', message_id='mock_001')

            c2 = Campaign.objects.create(
                name='VIP Offer',
                message='Exclusive VIP offer! Get 20% off all services this weekend.',
                sender_id='TextWave', status='sent', user=demo
            )
            for contact in Contact.objects.filter(user=demo, group=group2):
                CampaignRecipient.objects.create(campaign=c2, phone_number=contact.phone, status='delivered', message_id='mock_002')

            Campaign.objects.create(
                name='Monthly Newsletter',
                message='Hello! Check out our latest updates and new features this month.',
                sender_id='TextWave', status='draft', user=demo
            )

        if Transaction.objects.filter(user=demo).count() < 2:
            Transaction.objects.create(user=demo, amount='8.00', credits=1000, transaction_type='purchase', status='completed', description='Initial credit purchase')
            Transaction.objects.create(user=demo, amount='0.00', credits=-500, transaction_type='deduction', status='completed', description='SMS campaigns')

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully!'))
