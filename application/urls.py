from django.urls import path,include
from .import views

from .views import (
    Home,
)

urlpatterns = [
    path('', Home.as_view(), name = 'dashboard'),
    path('auth/', include('application.authentication.urls')),
    path('customer/', include('application.page_customer.urls')),
    path('product/', include('application.page_product.urls')),
    path('receiving/', include('application.page_receiving.urls')),
    path('releasing/', include('application.page_releasing.urls')),
    path('transaction/', include('application.page_transaction.urls')),
    path('full-search/', include('application.page_full_search.urls')),
    path('summary-report/', include('application.page_summary_report.urls')),
    # path('brand/', include('application.page_brand.urls')),
    # path('unit/', include('application.page_unit.urls')),
]
