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
    Unit,
    # Settings
)
from .forms import (
    UnitForm
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


class Unit_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/unit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Unit"
        return context

class Unit_Create(LoginRequiredMixin,TemplateView):
    template_name = 'components/unit_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Unit"
        return context

class Unit_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/unit_forms.html'
    def get(self, request):
        data = dict()
        form = UnitForm()
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
            form = UnitForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                data['url'] = reverse('unit')
        return JsonResponse(data)

class Unit_Update(LoginRequiredMixin,TemplateView):
    template_name = 'components/unit_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['unit'] = Unit.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Unit"
        return context

class Unit_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/unit_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        unit = Unit.objects.get(pk=id)
        form = UnitForm(instance=unit)
        context = {
            'form': form,
            'unit':unit,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "Save Changes",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Unit_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        unit = Unit.objects.get(pk=pk)
        if request.method == 'POST':
            form = UnitForm(request.POST,request.FILES,instance=unit)
            if form.is_valid():
                form.save()
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('unit')

        return JsonResponse(data)

class Unit_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Unit.objects.all()
    template_name = 'tables/unit_table.html'
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
            data['counter'] = self.queryset.filter(Q(name__icontains = search)).count()
            unit = self.queryset.filter(Q(name__icontains = search)).order_by('name')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'unit':unit,'start':start})
        return JsonResponse(data)
