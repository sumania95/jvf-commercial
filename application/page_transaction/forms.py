from django import forms
from django.forms import ModelForm
from application.models import (
    Customer,
    Transaction,
)



class TransactionCreateForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'customer',
            'brand',
            'model',
            'type',
            'khr',
            'engine_no',
            'chassis_no',
            'description',
            'condition',
            'date',
            'technician',
        ]

    def __init__(self,user=None, *args, **kwargs):
        print(user)
        super(TransactionCreateForm, self).__init__(*args, **kwargs)
        self.fields['customer']=forms.ModelChoiceField(queryset = Customer.objects.filter(branch=user.user_type.branch))


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'customer',
            'brand',
            'model',
            'type',
            'khr',
            'engine_no',
            'chassis_no',
            'description',
            'condition',
            'date',
            'technician',
        ]
