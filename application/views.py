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
        context['product_total'] = Product.objects.filter(branch=self.request.user.user_type.branch).count()
        context['customer_total'] = Customer.objects.filter(branch=self.request.user.user_type.branch).count()
        context['receiving_total'] = Receiving.objects.filter(branch=self.request.user.user_type.branch).count()
        context['releasing_total'] = Releasing.objects.filter(branch=self.request.user.user_type.branch).count()
        return context
