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
    Transaction,
)
from .forms import (
    TransactionForm,
    TransactionCreateForm
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


class Transaction_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/transaction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Transaction"
        return context

class Transaction_Create(LoginRequiredMixin,TemplateView):
    template_name = 'components/transaction_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Transaction"
        return context

class Transaction_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/transaction_forms.html'
    def get(self, request):
        data = dict()
        form = TransactionCreateForm(user=self.request.user)
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
            form = TransactionForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                form.instance.branch = self.request.user.user_type.branch
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                data['url'] = reverse('transaction')
        return JsonResponse(data)

class Transaction_Update(LoginRequiredMixin,TemplateView):
    template_name = 'components/transaction_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['transaction'] = Transaction.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Transaction"
        return context

class Transaction_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/transaction_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        transaction = Transaction.objects.get(pk=id)
        form = TransactionForm(instance=transaction)
        context = {
            'form': form,
            'transaction':transaction,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "Save Changes",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Transaction_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        transaction = Transaction.objects.get(pk=pk)
        if request.method == 'POST':
            form = TransactionForm(request.POST,request.FILES,instance=transaction)
            if form.is_valid():
                form.save()
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('transaction')

        return JsonResponse(data)

class Transaction_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Transaction.objects.all()
    template_name = 'tables/transaction_table.html'
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
            data['counter'] = self.queryset.filter(Q(description__icontains = search),branch=self.request.user.user_type.branch,date_created__range = [date_from,date_to]).count()
            transaction = self.queryset.filter(Q(description__icontains = search),branch=self.request.user.user_type.branch,date_created__range = [date_from,date_to]).order_by('date_created')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'transaction':transaction,'start':start})
        return JsonResponse(data)
