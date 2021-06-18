from django import forms
from django.forms import ModelForm
from application.models import (
    Unit,
)

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'name',
        ]
