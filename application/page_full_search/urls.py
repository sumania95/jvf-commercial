from django.urls import path,include
from .import views

from .views import (
    Full_Search_Page,
    Full_Search_Table_AJAXView,
)
# 127.0.0.1:8000/full_search/
urlpatterns = [
    path('', Full_Search_Page.as_view(), name = 'full_search'),
    path('api/table', Full_Search_Table_AJAXView.as_view(), name = 'full_search_table_api'),

]
