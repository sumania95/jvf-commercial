from django.urls import path,include
from .import views

from .views import (
    Product_Page,
    Product_Create,
    Product_Create_AJAXView,
    Product_Update,
    Product_Update_AJAXView,
    Product_Update_Save_AJAXView,
    Product_Table_AJAXView,
    Product_Export_Excel_AJAXView,
    Product_PDF_Print,
)
# 127.0.0.1:8000/product/
urlpatterns = [
    path('', Product_Page.as_view(), name = 'product'),
    path('create', Product_Create.as_view(), name = 'product_create'),
    path('api/create', Product_Create_AJAXView.as_view(), name = 'product_create_api'),
    path('update/<uuid:pk>', Product_Update.as_view(), name = 'product_update'),
    path('api/update/', Product_Update_AJAXView.as_view(), name = 'product_update_api'),
    path('api/update/save/<uuid:pk>', Product_Update_Save_AJAXView.as_view(), name = 'product_update_save_api'),
    path('api/table', Product_Table_AJAXView.as_view(), name = 'product_table_api'),
    path('export/product-list', Product_Export_Excel_AJAXView.as_view(), name = 'export_product'),
    path('reports/product/print/', Product_PDF_Print.as_view(), name = 'product_pdf_print'),

]
