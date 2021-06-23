from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
)

#functions
from django.db.models.functions import Coalesce,Concat
from django.db.models import Q,F,Sum,Count
from django.db.models import Value
from django.urls import reverse
#datetime
from datetime import datetime
#JSON AJAX
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Product,
    Customer,
    Receiving,
    Releasing,
)

class Home(LoginRequiredMixin,TemplateView):
    template_name = 'pages/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        receiving = Receiving.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('receiving_detail__quantity'),0))['quantity']
        releasing = Releasing.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('releasing_detail__quantity'),0))['quantity']
        context['check_balance'] = int(product)+int(releasing)-int(receiving)
        context['product_quantity_total'] = Product.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('quantity'),0))
        context['product_total'] = Product.objects.filter(branch=self.request.user.user_type.branch).count()
        context['customer_total'] = Customer.objects.filter(branch=self.request.user.user_type.branch).count()
        context['receiving_quantity_total'] = Receiving.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('receiving_detail__quantity'),0))
        context['receiving_total'] = Receiving.objects.filter(branch=self.request.user.user_type.branch).count()
        context['releasing_quantity_total'] = Releasing.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('releasing_detail__quantity'),0))
        context['releasing_total'] = Releasing.objects.filter(branch=self.request.user.user_type.branch).count()
        return context
