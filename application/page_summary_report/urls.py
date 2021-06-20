from django.urls import path,include
from django.conf.urls import url
from .import views

from .views import (
    Summary_Report_Page,
)
urlpatterns = [
    path('', Summary_Report_Page.as_view(), name = 'summary_report'),

]
