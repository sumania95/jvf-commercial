from django.urls import path,include
from django.conf.urls import url
from .import views

from .views import (
    Customer_Page,
    Customer_Create,
    Customer_Create_AJAXView,
    Customer_Update,
    Customer_Update_AJAXView,
    Customer_Update_Save_AJAXView,
    Customer_Table_AJAXView,
    Customer_Details_Page,
    Customer_Details_Table_AJAXView,

    # Customer_Print,
)
# 127.0.0.1:8000/product/
urlpatterns = [
    path('', Customer_Page.as_view(), name = 'customer'),
    path('create', Customer_Create.as_view(), name = 'customer_create'),
    path('api/create', Customer_Create_AJAXView.as_view(), name = 'customer_create_api'),
    path('update/<uuid:pk>', Customer_Update.as_view(), name = 'customer_update'),
    path('api/update/', Customer_Update_AJAXView.as_view(), name = 'customer_update_api'),
    path('api/update/save/<uuid:pk>', Customer_Update_Save_AJAXView.as_view(), name = 'customer_update_save_api'),
    path('api/table', Customer_Table_AJAXView.as_view(), name = 'customer_table_api'),
    path('details/<uuid:pk>/', Customer_Details_Page.as_view(), name = 'customer_detail'),
    path('api/details/table/<uuid:pk>/', Customer_Details_Table_AJAXView.as_view(), name = 'api_customer_detail'),
    # path('reports/print/<int:pk>', Customer_Print.as_view(), name = 'customer_print'),

]
