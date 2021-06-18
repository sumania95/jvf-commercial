from django.urls import path,include
from django.conf.urls import url
from .import views

from .views import (
    Releasing_Page,
    Releasing_Create,
    Releasing_Create_AJAXView,
    Releasing_Update,
    Releasing_Update_AJAXView,
    Releasing_Update_Save_AJAXView,
    Releasing_Table_AJAXView,
    Releasing_Details_Page,
    Releasing_Details_Form_AJAXView,
    Releasing_Details_Form_Item_AJAXView,
    Releasing_Details_Form_Item_Save_AJAXView,
    Releasing_Details_Form_Item_Delete_Save_AJAXView,
    Releasing_Details_Form_Product_Table_AJAXView,
    Releasing_Details_Table_AJAXView,
    Releasing_Detail_PDF_Print,
    # Releasing_Print,
)
# 127.0.0.1:8000/product/
urlpatterns = [
    path('', Releasing_Page.as_view(), name = 'releasing'),
    path('create', Releasing_Create.as_view(), name = 'releasing_create'),
    path('api/create', Releasing_Create_AJAXView.as_view(), name = 'releasing_create_api'),
    path('update/<uuid:pk>', Releasing_Update.as_view(), name = 'releasing_update'),
    path('api/update/', Releasing_Update_AJAXView.as_view(), name = 'releasing_update_api'),
    path('api/update/save/<uuid:pk>', Releasing_Update_Save_AJAXView.as_view(), name = 'releasing_update_save_api'),
    path('api/table', Releasing_Table_AJAXView.as_view(), name = 'releasing_table_api'),
    path('details/<uuid:pk>/', Releasing_Details_Page.as_view(), name = 'releasing_detail'),
    path('api/details/table/<uuid:pk>/', Releasing_Details_Table_AJAXView.as_view(), name = 'api_releasing_detail'),
    path('api/details/create/', Releasing_Details_Form_AJAXView.as_view(), name = 'api_releasing_detail_form'),
    path('api/details/create/item/<uuid:pk>', Releasing_Details_Form_Item_AJAXView.as_view(), name = 'api_releasing_detail_form_item'),
    path('api/details/create/item/save', Releasing_Details_Form_Item_Save_AJAXView.as_view(), name = 'api_releasing_detail_form_item_save'),
    path('api/details/create/item/remove/save/<uuid:pk>', Releasing_Details_Form_Item_Delete_Save_AJAXView.as_view(), name = 'api_releasing_detail_form_item_delete_save'),
    path('api/details/create/table', Releasing_Details_Form_Product_Table_AJAXView.as_view(), name = 'api_releasing_detail_form_table'),
    path('report/pdf/pull-out-form/<uuid:pk>', Releasing_Detail_PDF_Print.as_view(), name = 'releasing_report_pdf'),
    # path('reports/print/<int:pk>', Releasing_Print.as_view(), name = 'releasing_print'),

]
