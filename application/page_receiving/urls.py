from django.urls import path,include
from django.conf.urls import url
from .import views

from .views import (
    Receiving_Page,
    Receiving_Create,
    Receiving_Create_AJAXView,
    Receiving_Update,
    Receiving_Update_AJAXView,
    Receiving_Update_Save_AJAXView,
    Receiving_Table_AJAXView,
    Receiving_Details_Page,
    Receiving_Details_Form_AJAXView,
    Receiving_Details_Form_Item_AJAXView,
    Receiving_Details_Form_Item_Save_AJAXView,
    Receiving_Details_Form_Item_Delete_Save_AJAXView,
    Receiving_Details_Form_Product_Table_AJAXView,
    Receiving_Details_Table_AJAXView,
    Receiving_Detail_PDF_Print,
    # Receiving_Print,
)
# 127.0.0.1:8000/product/
urlpatterns = [
    path('', Receiving_Page.as_view(), name = 'receiving'),
    path('create', Receiving_Create.as_view(), name = 'receiving_create'),
    path('api/create', Receiving_Create_AJAXView.as_view(), name = 'receiving_create_api'),
    path('update/<uuid:pk>', Receiving_Update.as_view(), name = 'receiving_update'),
    path('api/update/', Receiving_Update_AJAXView.as_view(), name = 'receiving_update_api'),
    path('api/update/save/<uuid:pk>', Receiving_Update_Save_AJAXView.as_view(), name = 'receiving_update_save_api'),
    path('api/table', Receiving_Table_AJAXView.as_view(), name = 'receiving_table_api'),
    path('details/<uuid:pk>/', Receiving_Details_Page.as_view(), name = 'receiving_detail'),
    path('api/details/table/<uuid:pk>/', Receiving_Details_Table_AJAXView.as_view(), name = 'api_receiving_detail'),
    path('api/details/create/', Receiving_Details_Form_AJAXView.as_view(), name = 'api_receiving_detail_form'),
    path('api/details/create/item/<uuid:pk>', Receiving_Details_Form_Item_AJAXView.as_view(), name = 'api_receiving_detail_form_item'),
    path('api/details/create/item/save', Receiving_Details_Form_Item_Save_AJAXView.as_view(), name = 'api_receiving_detail_form_item_save'),
    path('api/details/create/item/remove/save/<uuid:pk>', Receiving_Details_Form_Item_Delete_Save_AJAXView.as_view(), name = 'api_receiving_detail_form_item_delete_save'),
    path('api/details/create/table', Receiving_Details_Form_Product_Table_AJAXView.as_view(), name = 'api_receiving_detail_form_table'),
    path('reports/pdf/receiving-report/<uuid:pk>/', Receiving_Detail_PDF_Print.as_view(), name = 'receiving_report_pdf'),

    # path('reports/print/<int:pk>', Receiving_Print.as_view(), name = 'receiving_print'),

]
