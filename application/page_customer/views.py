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
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin
from application.models import (
    Customer,
    Transaction,
)
from .forms import (
    CustomerForm,
)
from application.render import (
    Render
)
from django.utils import timezone
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'


class Customer_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Customer"
        return context

class Customer_Create(LoginRequiredMixin,TemplateView):
    template_name = 'components/customer_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Customer"
        return context

class Customer_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/customer_forms.html'
    def get(self, request):
        data = dict()
        form = CustomerForm()
        context = {
            'form': form,
            'is_Create': True,
            'btn_name': "primary",
            'btn_title': "Submit & Save",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)
    def post(self, request):
        data =  dict()
        if request.method == 'POST':
            form = CustomerForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                form.instance.branch = self.request.user.user_type.branch
                stock = form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                data['url'] = reverse('customer')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'
        return JsonResponse(data)

class Customer_Update(LoginRequiredMixin,TemplateView):
    template_name = 'components/customer_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['customer'] = Customer.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Customer"
        return context

class Customer_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/customer_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        customer = Customer.objects.get(pk=id)
        form = CustomerForm(instance=customer)
        context = {
            'form': form,
            'customer':customer,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "Save Changes",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Customer_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        customer = Customer.objects.get(pk=pk)
        if request.method == 'POST':
            form = CustomerForm(request.POST,request.FILES,instance=customer)
            if form.is_valid():
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('customer')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'

        return JsonResponse(data)


class Customer_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Customer.objects.all()
    template_name = 'tables/customer_table.html'
    def get(self, request):
        data = dict()
        try:
            search = self.request.GET.get('search')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
        except KeyError:
            search = None
            start = None
            end = None
        if search or start or end:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(Q(name__icontains = search),branch=self.request.user.user_type.branch).count()
            customer = self.queryset.filter(Q(name__icontains = search),branch=self.request.user.user_type.branch).order_by('name')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'customer':customer,'start':start})
        return JsonResponse(data)

class Customer_Details_Page(DetailView):
    model = Customer
    template_name = 'pages/customer_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Transaction Details"
        return context

class Customer_Details_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Transaction.objects.all()
    template_name = 'tables/transaction_details_customer_table.html'
    def get(self, request,pk):
        data = dict()
        try:
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
        except KeyError:
            start = None
            end = None
        if start or end:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(customer__id=pk).count()
            transaction = self.queryset.filter(customer__id=pk).order_by('-date')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'transaction':transaction,'start':start})
        return JsonResponse(data)
