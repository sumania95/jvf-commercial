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

from django.utils import timezone
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'

class Full_Search_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/full_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Full Search Products"
        return context

class Full_Search_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Product.objects.all()
    template_name = 'tables/full_search_table.html'
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
            data['counter'] = self.queryset.filter(Q(part_number__icontains = search)|Q(description__icontains = search)).count()
            product = self.queryset.filter(Q(part_number__icontains = search)|Q(description__icontains = search)).order_by('description','part_number')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'product':product,'start':start})
        return JsonResponse(data)
