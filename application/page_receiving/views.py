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
    Receiving,
    Receiving_Detail,
    User_Type,
)
from .forms import (
    ReceivingForm,
    Receiving_DetailForm
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


class Receiving_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/receiving.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Receiving"
        return context

class Receiving_Create(LoginRequiredMixin,TemplateView):
    template_name = 'components/receiving_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Receiving"
        return context

class Receiving_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/receiving_forms.html'
    def get(self, request):
        data = dict()
        form = ReceivingForm()
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
            form = ReceivingForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                form.instance.branch = self.request.user.user_type.branch
                stock = form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                print(form.instance.id)
                data['url'] = reverse('receiving_detail',kwargs={'pk': stock.id})
        return JsonResponse(data)

class Receiving_Update(LoginRequiredMixin,TemplateView):
    template_name = 'components/receiving_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['receiving'] = Receiving.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Receiving"
        return context

class Receiving_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/receiving_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        receiving = Receiving.objects.get(pk=id)
        form = ReceivingForm(instance=receiving)
        context = {
            'form': form,
            'receiving':receiving,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "Save Changes",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Receiving_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        receiving = Receiving.objects.get(pk=pk)
        if request.method == 'POST':
            form = ReceivingForm(request.POST,request.FILES,instance=receiving)
            if form.is_valid():
                form.save()
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('receiving')

        return JsonResponse(data)


class Receiving_Table_AJAXView(LoginRequiredMixin,View):
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

class Receiving_Details_Page(DetailView):
    model = Receiving
    template_name = 'pages/receiving_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Details Overview"
        return context

class Receiving_Details_Form_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/receiving_details_forms.html'
    def get(self, request):
        data = dict()
        try:
            receiving_id = self.request.GET.get('receiving_id')
        except Exception as e:
            receiving_id = None
        context = {
            'receiving_id': receiving_id,
            'is_Create': True,
            'btn_name': "primary",
            'btn_title': "Submit",
            'title': "Product List",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Receiving_Details_Form_Product_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Product.objects.all()
    template_name = 'tables/receiving_details_form_product_table.html'
    def get(self, request):
        data = dict()
        try:
            search = self.request.GET.get('search')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            receiving_id = self.request.GET.get('receiving_id')
        except KeyError:
            search = None
            start = None
            end = None
            receiving_id = None
        if search or start or end:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.exclude(id__in = Receiving_Detail.objects.values('product_id').filter(receiving_id = receiving_id)).filter(Q(description__icontains = search)|Q(part_number__icontains = search)).count()
            product = self.queryset.exclude(id__in = Receiving_Detail.objects.values('product_id').filter(receiving_id = receiving_id)).filter(Q(description__icontains = search)|Q(part_number__icontains = search)).order_by('description','part_number')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'product':product,'start':start,'receiving_id':receiving_id})
        return JsonResponse(data)

class Receiving_Details_Form_Item_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/receiving_details_forms_item.html'
    def get(self, request,pk):
        data = dict()
        try:
            receiving_id = self.request.GET.get('receiving_id')
        except KeyError:
            receiving_id = None
        product = Product.objects.get(id=pk)
        form = Receiving_DetailForm()
        context = {
            'receiving_id': receiving_id,
            'product': product,
            'form': form,
            'is_Create': True,
            'btn_name': "primary",
            'btn_title': "Submit",
            'title': "Product List",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Receiving_Details_Form_Item_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request):
        data = dict()
        try:
            product_id = self.request.POST.get('product_id')
            receiving_id = self.request.POST.get('receiving_id')
        except KeyError:
            product_id = None
            receiving_id = None
        if request.method == 'POST':
            form = Receiving_DetailForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.product_id = product_id
                form.instance.receiving_id = receiving_id
                product_form = form.save()
                Product.objects.filter(id=product_id).update(quantity=F('quantity')+(product_form.quantity))
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
        return JsonResponse(data)

class Receiving_Details_Form_Item_Delete_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data =  dict()
        receiving_detail = Receiving_Detail.objects.get(id=pk)
        if request.method == 'POST':
            Product.objects.filter(id=receiving_detail.product_id).update(quantity=F('quantity')-(receiving_detail.quantity))
            Receiving_Detail.objects.get(id=receiving_detail.id).delete()
            data['message_type'] = success
            data['message_title'] = 'Successfully removed.'
        return JsonResponse(data)

class Receiving_Details_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Receiving_Detail.objects.all()
    template_name = 'tables/receiving_details_table.html'
    def get(self, request,pk):
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
            data['counter'] = self.queryset.filter(Q(product__description__icontains = search),receiving__id=pk).count()
            receiving = self.queryset.filter(Q(product__description__icontains = search),receiving__id=pk).order_by('date_created')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'receiving':receiving,'start':start})
        return JsonResponse(data)

from application.render import (
    Render,
)

class Receiving_Detail_PDF_Print(LoginRequiredMixin,View):
    queryset = Receiving_Detail.objects.all()
    def get(self, request,pk):
        receiving = Receiving.objects.get(id=pk)
        receiving_detail = self.queryset.filter(receiving=receiving)
        now = timezone.now()
        user = User_Type.objects.filter(branch=self.request.user.user_type.branch).first()
        params = {
            'now': now,
            'user': user,
            'receiving_detail': receiving_detail,
            'receiving': receiving,
        }
        pdf = Render.render('reports/receiving_report_PDF_print.html', params)
        return pdf
