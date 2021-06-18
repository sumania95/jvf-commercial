from django import forms
from django.forms import ModelForm
from application.models import (
    Customer,
)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name',
            'address',
            'category',
        ]
