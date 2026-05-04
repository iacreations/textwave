from django import forms

CREDIT_PACKAGES = [
    ('100', '100 Credits - $1.00'),
    ('500', '500 Credits - $4.50'),
    ('1000', '1000 Credits - $8.00'),
    ('5000', '5000 Credits - $35.00'),
]

class PurchaseForm(forms.Form):
    package = forms.ChoiceField(
        choices=CREDIT_PACKAGES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Select Package'
    )
    payment_method = forms.ChoiceField(
        choices=[('card', 'Credit/Debit Card'), ('mobile', 'Mobile Money')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    card_number = forms.CharField(
        max_length=19, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456'}),
    )
