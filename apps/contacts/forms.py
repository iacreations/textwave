from django import forms
from .models import Contact, ContactGroup

class ContactGroupForm(forms.ModelForm):
    class Meta:
        model = ContactGroup
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'phone', 'email', 'group')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = ContactGroup.objects.filter(user=user)
        self.fields['group'].required = False

class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'}),
        help_text='CSV file with columns: name, phone, email (optional), group (optional)'
    )
    group = forms.ModelChoiceField(
        queryset=ContactGroup.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Assign all imported contacts to this group (optional)'
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = ContactGroup.objects.filter(user=user)
