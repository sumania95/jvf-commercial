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
    Product,
    Branch,
)
from .forms import (
    ProductForm
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


class Product_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Product"
        return context

class Product_Create(LoginRequiredMixin,TemplateView):
    template_name = 'components/product_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Product"
        return context

class Product_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/product_forms.html'
    def get(self, request):
        data = dict()
        form = ProductForm()
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
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                form.instance.branch = self.request.user.user_type.branch
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                data['url'] = reverse('product')
        return JsonResponse(data)

class Product_Update(LoginRequiredMixin,TemplateView):
    template_name = 'components/product_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['product'] = Product.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Product"
        return context

class Product_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/product_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        product = Product.objects.get(pk=id)
        form = ProductForm(instance=product)
        context = {
            'form': form,
            'product':product,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "Save Changes",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Product_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        product = Product.objects.get(pk=pk)
        if request.method == 'POST':
            form = ProductForm(request.POST,request.FILES,instance=product)
            if form.is_valid():
                form.save()
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('product')

        return JsonResponse(data)

class Product_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Product.objects.all()
    template_name = 'tables/product_table.html'
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
            data['counter'] = self.queryset.filter(Q(part_number__icontains = search)|Q(description__icontains = search),branch=self.request.user.user_type.branch).count()
            product = self.queryset.filter(Q(part_number__icontains = search)|Q(description__icontains = search),branch=self.request.user.user_type.branch).order_by('description','part_number')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'product':product,'start':start})
        return JsonResponse(data)

import csv
from django.http import HttpResponse

class Product_Export_Excel_AJAXView(LoginRequiredMixin,View):
    def get(self, request):
        products = Product.objects.filter(branch=self.request.user.user_type.branch).values_list('part_number', 'description', 'brand__brand','location','quantity', 'unit_price').order_by('brand__brand','description','part_number')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="programs.csv"'
        writer = csv.writer(response)
        writer.writerow(['PART NUMBER', 'DESCRIPTION', 'BRAND','LOCATION' ,'STOCKS','PRICE (JPY/USD)'])
        for product in products:
            writer.writerow(product)
        return response

from application.render import (
    Render,
)

class Product_PDF_Print(LoginRequiredMixin,View):
    queryset = Product.objects.all()
    def get(self, request):
        product = self.queryset.filter(branch=self.request.user.user_type.branch).order_by('brand__brand','description','part_number')
        now = timezone.now()
        user = Branch.objects.filter(branch=self.request.user.user_type.branch).first()
        params = {
            'now': now,
            'user': user,
            'product': product,
        }
        pdf = Render.render('reports/product_PDF_print.html', params)
        return pdf
