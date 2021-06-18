from django import forms
from django.forms import ModelForm
from application.models import (
    Receiving,
    Receiving_Detail,
)

class ReceivingForm(forms.ModelForm):
    class Meta:
        model = Receiving
        fields = [
            'control_no',
            'invoice_no',
            'vendor',
            'shipped_via',
            'remarks',
        ]

class Receiving_DetailForm(forms.ModelForm):
    class Meta:
        model = Receiving_Detail
        fields = [
            'quantity',
            'condition',
        ]
