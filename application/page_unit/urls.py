from django.urls import path,include
from .import views

from .views import (
    Unit_Page,
    Unit_Create,
    Unit_Create_AJAXView,
    Unit_Update,
    Unit_Update_AJAXView,
    Unit_Update_Save_AJAXView,
    Unit_Table_AJAXView,
    # Unit_Print,
)
# 127.0.0.1:8000/product/
urlpatterns = [
    path('', Unit_Page.as_view(), name = 'unit'),
    path('create', Unit_Create.as_view(), name = 'unit_create'),
    path('api/create', Unit_Create_AJAXView.as_view(), name = 'unit_create_api'),
    path('update/<uuid:pk>', Unit_Update.as_view(), name = 'unit_update'),
    path('api/update/', Unit_Update_AJAXView.as_view(), name = 'unit_update_api'),
    path('api/update/save/<uuid:pk>', Unit_Update_Save_AJAXView.as_view(), name = 'unit_update_save_api'),
    path('api/table', Unit_Table_AJAXView.as_view(), name = 'unit_table_api'),
    # path('reports/print/<int:pk>', Unit_Print.as_view(), name = 'unit_print'),

]
