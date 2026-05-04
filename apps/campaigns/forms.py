from django import forms
from .models import Campaign
from apps.contacts.models import ContactGroup

class CampaignForm(forms.ModelForm):
    recipient_type = forms.ChoiceField(
        choices=[('groups', 'From Groups'), ('manual', 'Manual Numbers')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='manual'
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=ContactGroup.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
    manual_numbers = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter phone numbers, one per line or comma-separated'}),
    )
    send_option = forms.ChoiceField(
        choices=[('now', 'Send Now'), ('schedule', 'Schedule'), ('draft', 'Save as Draft')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='now'
    )

    class Meta:
        model = Campaign
        fields = ('name', 'sender_id', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sender_id': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'id': 'message-textarea'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].queryset = ContactGroup.objects.filter(user=user)
        self.fields['sender_id'].initial = user.profile.sender_id if hasattr(user, 'profile') else 'TextWave'

    def clean(self):
        cleaned_data = super().clean()
        recipient_type = cleaned_data.get('recipient_type')
        if recipient_type == 'groups' and not cleaned_data.get('groups'):
            self.add_error('groups', 'Please select at least one group.')
        elif recipient_type == 'manual' and not cleaned_data.get('manual_numbers'):
            self.add_error('manual_numbers', 'Please enter at least one phone number.')
        return cleaned_data
