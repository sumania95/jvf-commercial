from django import forms
from django.forms import ModelForm
from application.models import (
    Product,
)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'part_number',
            'description',
            'brand',
            'location',
            'currency',
            'unit_price',
        ]
