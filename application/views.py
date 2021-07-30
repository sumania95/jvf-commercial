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
    Receiving_Detail,
    Releasing,
)

class Home(LoginRequiredMixin,TemplateView):
    template_name = 'pages/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('quantity'),0))['quantity']
        receiving = Receiving.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('receiving_detail__quantity'),0))['quantity']
        releasing = Releasing.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('releasing_detail__quantity'),0))['quantity']

        product_sum = Product.objects.filter(branch=self.request.user.user_type.branch).aggregate(Sum('quantity'))

        receiving_sum = Receiving.objects.filter(branch=self.request.user.user_type.branch).aggregate(Sum('receiving_detail__quantity'))
        print(product_sum)
        print(receiving_sum)
        # product_decrease = Product.objects.filter(quantity__lt=0).all()
        # for p in product_decrease:
        #     print(p.description + " - " + p.part_number)
        print(releasing)
        print(product)
        print(receiving)
        total = int(product)+int(releasing)-int(receiving)
        print(total)
        context['check_balance'] = int(product)+int(releasing)-int(receiving)
        context['product_quantity_total'] = Product.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('quantity'),0))
        context['product_total'] = Product.objects.filter(branch=self.request.user.user_type.branch).count()
        context['customer_total'] = Customer.objects.filter(branch=self.request.user.user_type.branch).count()
        context['receiving_quantity_total'] = Receiving.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('receiving_detail__quantity'),0))
        context['receiving_total'] = Receiving.objects.filter(branch=self.request.user.user_type.branch).count()
        context['releasing_quantity_total'] = Releasing.objects.filter(branch=self.request.user.user_type.branch).aggregate(quantity=Coalesce(Sum('releasing_detail__quantity'),0))
        context['releasing_total'] = Releasing.objects.filter(branch=self.request.user.user_type.branch).count()
        return context
