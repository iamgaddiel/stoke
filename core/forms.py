from django import forms
from .models import TransactionHistory



class SendCryptoModelForm(forms.ModelForm):
    class Meta:
        model = TransactionHistory
        exclude = ['transaction_ref', 'transaction_type', 'from_address', 'to_address']
