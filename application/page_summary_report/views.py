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
