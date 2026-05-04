from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'), ('scheduled', 'Scheduled'), ('sending', 'Sending'),
        ('sent', 'Sent'), ('failed', 'Failed'),
    ]
    name = models.CharField(max_length=200)
    message = models.TextField()
    sender_id = models.CharField(max_length=11, default='TextWave')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def total_recipients(self):
        return self.recipients.count()

    def sent_count(self):
        return self.recipients.filter(status='sent').count()

    def delivered_count(self):
        return self.recipients.filter(status='delivered').count()

    def failed_count(self):
        return self.recipients.filter(status='failed').count()

    def pending_count(self):
        return self.recipients.filter(status='pending').count()

class CampaignRecipient(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('sent', 'Sent'), ('delivered', 'Delivered'), ('failed', 'Failed'),
    ]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='recipients')
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message_id = models.CharField(max_length=100, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.status}"
