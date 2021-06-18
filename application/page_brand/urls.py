from django.urls import path,include
from .import views

from .views import (
    Brand_Page,
    Brand_Create,
    Brand_Create_AJAXView,
    Brand_Update,
    Brand_Update_AJAXView,
    Brand_Update_Save_AJAXView,
    Brand_Table_AJAXView,
    # Brand_Print,
)
# 127.0.0.1:8000/brand/
urlpatterns = [
    path('', Brand_Page.as_view(), name = 'brand'),
    path('create', Brand_Create.as_view(), name = 'brand_create'),
    path('api/create', Brand_Create_AJAXView.as_view(), name = 'brand_create_api'),
    path('update/<uuid:pk>', Brand_Update.as_view(), name = 'brand_update'),
    path('api/update/', Brand_Update_AJAXView.as_view(), name = 'brand_update_api'),
    path('api/update/save/<uuid:pk>', Brand_Update_Save_AJAXView.as_view(), name = 'brand_update_save_api'),
    path('api/table', Brand_Table_AJAXView.as_view(), name = 'brand_table_api'),
    # path('reports/print/<int:pk>', Brand_Print.as_view(), name = 'brand_print'),

]
