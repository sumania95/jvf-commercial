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
    Releasing,
    Releasing_Detail,
    User_Type,
    # Settings
)
from .forms import (
    ReleasingForm,
    Releasing_DetailForm
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


class Releasing_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/releasing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Releasing"
        return context

class Releasing_Create(LoginRequiredMixin,TemplateView):
    template_name = 'components/releasing_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Releasing"
        return context

class Releasing_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/releasing_forms.html'
    def get(self, request):
        data = dict()
        form = ReleasingForm()
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
            form = ReleasingForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                form.instance.branch = self.request.user.user_type.branch
                stock = form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                print(form.instance.id)
                data['url'] = reverse('releasing_detail',kwargs={'pk': stock.id})
        return JsonResponse(data)

class Releasing_Update(LoginRequiredMixin,TemplateView):
    template_name = 'components/releasing_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['releasing'] = Releasing.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Releasing"
        return context

class Releasing_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/releasing_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        releasing = Releasing.objects.get(pk=id)
        form = ReleasingForm(instance=releasing)
        context = {
            'form': form,
            'releasing':releasing,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "Save Changes",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Releasing_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        releasing = Releasing.objects.get(pk=pk)
        if request.method == 'POST':
            form = ReleasingForm(request.POST,request.FILES,instance=releasing)
            if form.is_valid():
                form.save()
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('releasing')

        return JsonResponse(data)


class Releasing_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Releasing.objects.all()
    template_name = 'tables/releasing_table.html'
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
            data['counter'] = self.queryset.filter(branch=self.request.user.user_type.branch,date_created__range = [date_from,date_to]).count()
            releasing = self.queryset.filter(branch=self.request.user.user_type.branch,date_created__range = [date_from,date_to]).annotate(number_of_releasing_detail=Sum('releasing_detail__quantity')).order_by('-date_created')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'releasing':releasing,'start':start})
        return JsonResponse(data)

class Releasing_Details_Page(DetailView):
    model = Releasing
    template_name = 'pages/releasing_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Details Overview"
        return context

class Releasing_Details_Form_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/releasing_details_forms.html'
    def get(self, request):
        data = dict()
        try:
            releasing_id = self.request.GET.get('releasing_id')
        except Exception as e:
            releasing_id = None
        context = {
            'releasing_id': releasing_id,
            'is_Create': True,
            'btn_name': "primary",
            'btn_title': "Submit",
            'title': "Product List",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Releasing_Details_Form_Product_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Product.objects.all()
    template_name = 'tables/releasing_details_form_product_table.html'
    def get(self, request):
        data = dict()
        try:
            search = self.request.GET.get('search')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
            releasing_id = self.request.GET.get('releasing_id')
        except KeyError:
            search = None
            start = None
            end = None
            releasing_id = None
        if search or start or end:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.exclude(id__in = Releasing_Detail.objects.values('product_id').filter(releasing_id = releasing_id)).filter(Q(description__icontains = search)|Q(part_number__icontains = search)).count()
            product = self.queryset.exclude(id__in = Releasing_Detail.objects.values('product_id').filter(releasing_id = releasing_id)).filter(Q(description__icontains = search)|Q(part_number__icontains = search)).order_by('description','part_number')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'product':product,'start':start,'releasing_id':releasing_id})
        return JsonResponse(data)

class Releasing_Details_Form_Item_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/releasing_details_forms_item.html'
    def get(self, request,pk):
        data = dict()
        try:
            releasing_id = self.request.GET.get('releasing_id')
        except KeyError:
            releasing_id = None
        product = Product.objects.get(id=pk)
        form = Releasing_DetailForm()
        context = {
            'releasing_id': releasing_id,
            'product': product,
            'form': form,
            'is_Create': True,
            'btn_name': "primary",
            'btn_title': "Submit",
            'title': "Product List",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Releasing_Details_Form_Item_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request):
        data = dict()
        try:
            product_id = self.request.POST.get('product_id')
            releasing_id = self.request.POST.get('releasing_id')
        except KeyError:
            product_id = None
            releasing_id = None
        if request.method == 'POST':
            form = Releasing_DetailForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.product_id = product_id
                form.instance.releasing_id = releasing_id
                product_form = form.save()
                Product.objects.filter(id=product_id).update(quantity=F('quantity')-(product_form.quantity))
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
        return JsonResponse(data)

class Releasing_Details_Form_Item_Delete_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data =  dict()
        releasing_detail = Releasing_Detail.objects.get(id=pk)
        if request.method == 'POST':
            Product.objects.filter(id=releasing_detail.product_id).update(quantity=F('quantity')+(releasing_detail.quantity))
            Releasing_Detail.objects.get(id=releasing_detail.id).delete()
            data['message_type'] = success
            data['message_title'] = 'Successfully removed.'
        return JsonResponse(data)

class Releasing_Details_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Releasing_Detail.objects.all()
    template_name = 'tables/releasing_details_table.html'
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
            data['counter'] = self.queryset.filter(Q(product__description__icontains = search),releasing__id=pk).count()
            releasing = self.queryset.filter(Q(product__description__icontains = search),releasing__id=pk).order_by('date_created')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'releasing':releasing,'start':start})
        return JsonResponse(data)

from application.render import (
    Render,
)

class Releasing_Detail_PDF_Print(LoginRequiredMixin,View):
    queryset = Releasing_Detail.objects.all()
    def get(self, request,pk):
        releasing = Releasing.objects.get(id=pk)
        releasing_detail = self.queryset.filter(releasing=releasing)
        now = timezone.now()
        user = User_Type.objects.filter(branch=self.request.user.user_type.branch).first()
        params = {
            'now': now,
            'user': user,
            'releasing_detail': releasing_detail,
            'releasing': releasing,
        }
        pdf = Render.render('reports/pull_out_form_PDF_print.html', params)
        return pdf
