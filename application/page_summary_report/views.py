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
    Receiving,
    Releasing,
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


class Summary_Report_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/summary_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Summary Report"
        return context

class Summary_Receiving_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Receiving.objects.all()
    template_name = 'tables/receiving_table.html'
    def get(self, request):
        data = dict()
        try:
            search = self.request.GET.get('search')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            datepicker1 = self.request.GET.get('datepicker1')
            datepicker2 = self.request.GET.get('datepicker2')
        except KeyError:
            search = None
            start = None
            end = None
            datepicker1 = None
            datepicker2 = None
        date_from = datetime.strptime(datepicker1+' 00:00:00', "%Y-%m-%d %H:%M:%S")
        date_to = datetime.strptime(datepicker2+' 23:59:59', "%Y-%m-%d %H:%M:%S")
        if search or start or end or date_from or date_to:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(Q(vendor__icontains = search),branch=self.request.user.user_type.branch,date_created__range = [date_from,date_to]).count()
            receiving = self.queryset.filter(Q(vendor__icontains = search),branch=self.request.user.user_type.branch,date_created__range = [date_from,date_to]).annotate(number_of_receiving_detail=Sum('receiving_detail__quantity')).order_by('-date_created')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'receiving':receiving,'start':start})
        return JsonResponse(data)

class Summary_Releasing_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Receiving.objects.all()
    template_name = 'tables/receiving_table.html'
    def get(self, request):
        data = dict()
        try:
            search = self.request.GET.get('search')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            datepicker1 = self.request.GET.get('datepicker1')
            datepicker2 = self.request.GET.get('datepicker2')
        except KeyError:
            search = None
            start = None
            end = None
            datepicker1 = None
            datepicker2 = None
        date_from = datetime.strptime(datepicker1+' 00:00:00', "%Y-%m-%d %H:%M:%S")
        date_to = datetime.strptime(datepicker2+' 23:59:59', "%Y-%m-%d %H:%M:%S")
        if search or start or end or date_from or date_to:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(Q(vendor__icontains = search),branch=self.request.user.user_type.branch,date_created__range = [date_from,date_to]).count()
            receiving = self.queryset.filter(Q(vendor__icontains = search),branch=self.request.user.user_type.branch,date_created__range = [date_from,date_to]).annotate(number_of_receiving_detail=Sum('receiving_detail__quantity')).order_by('-date_created')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'receiving':receiving,'start':start})
        return JsonResponse(data)
