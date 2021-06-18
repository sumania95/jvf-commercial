from django import forms
from django.forms import ModelForm
from application.models import (
    Releasing,
    Releasing_Detail,
)

class ReleasingForm(forms.ModelForm):
    class Meta:
        model = Releasing
        fields = [
            'control_no',
            'category',
            'customer_name',
            'purchase_order_number',
            'others',
        ]

class Releasing_DetailForm(forms.ModelForm):
    class Meta:
        model = Releasing_Detail
        fields = [
            'quantity',
        ]
