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
    Brand,
)
from .forms import (
    BrandForm
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


class Brand_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/brand.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Brand"
        return context

class Brand_Create(LoginRequiredMixin,TemplateView):
    template_name = 'components/brand_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Brand"
        return context

class Brand_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/brand_forms.html'
    def get(self, request):
        data = dict()
        form = BrandForm()
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
            form = BrandForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                data['url'] = reverse('brand')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'
        return JsonResponse(data)

class Brand_Update(LoginRequiredMixin,TemplateView):
    template_name = 'components/brand_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['brand'] = Brand.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Brand"
        return context

class Brand_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/brand_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        brand = Brand.objects.get(pk=id)
        form = BrandForm(instance=brand)
        context = {
            'form': form,
            'brand':brand,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "Save Changes",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Brand_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        brand = Brand.objects.get(pk=pk)
        if request.method == 'POST':
            form = BrandForm(request.POST,request.FILES,instance=brand)
            if form.is_valid():
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('brand')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'

        return JsonResponse(data)

class Brand_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Brand.objects.all()
    template_name = 'tables/brand_table.html'
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
            data['counter'] = self.queryset.filter(Q(brand__icontains = search)).count()
            brand = self.queryset.filter(Q(brand__icontains = search)).order_by('brand')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'brand':brand,'start':start})
        return JsonResponse(data)
