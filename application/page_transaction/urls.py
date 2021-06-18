from django.urls import path,include
from .import views

from .views import (
    Transaction_Page,
    Transaction_Create,
    Transaction_Create_AJAXView,
    Transaction_Update,
    Transaction_Update_AJAXView,
    Transaction_Update_Save_AJAXView,
    Transaction_Table_AJAXView,
    # Transaction_Print,
)
# 127.0.0.1:8000/transaction/
urlpatterns = [
    path('', Transaction_Page.as_view(), name = 'transaction'),
    path('create', Transaction_Create.as_view(), name = 'transaction_create'),
    path('api/create', Transaction_Create_AJAXView.as_view(), name = 'transaction_create_api'),
    path('update/<uuid:pk>', Transaction_Update.as_view(), name = 'transaction_update'),
    path('api/update/', Transaction_Update_AJAXView.as_view(), name = 'transaction_update_api'),
    path('api/update/save/<uuid:pk>', Transaction_Update_Save_AJAXView.as_view(), name = 'transaction_update_save_api'),
    path('api/table', Transaction_Table_AJAXView.as_view(), name = 'transaction_table_api'),
    # path('reports/print/<int:pk>', Transaction_Print.as_view(), name = 'transaction_print'),

]
