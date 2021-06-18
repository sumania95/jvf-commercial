from django import forms
from django.forms import ModelForm
from application.models import (
    Brand,
)

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = [
            'brand',
        ]
