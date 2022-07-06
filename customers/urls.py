from django.urls import path
from . import views
from .api.views import CustomersListAPIView

urlpatterns = [
    path('', views.load_json_or_csv),
    path('customers/', CustomersListAPIView.as_view(), name='customers'),
    path(
        'customers/<str:regiao>/<str:customer_type>/', 
        CustomersListAPIView.as_view(), name='customers_region_and_type'),
    path(
        'customers/<str:region_or_customer_type>/', 
        CustomersListAPIView.as_view(), name='customers_region_or_type')
]
