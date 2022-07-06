from rest_framework import generics

from customers.models import CustomerModel
from .serializers import CustomerSerializer


class CustomersListAPIView(generics.ListAPIView):

    queryset = CustomerModel.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        if self.kwargs.get('regiao') and self.kwargs.get('customer_type'):

            return self.queryset.filter(
                customer_type=self.kwargs.get('customer_type'),
                location__region=self.kwargs.get('regiao'))

        elif self.kwargs.get('region_or_customer_type'):
            region_queryset = self.queryset.filter(
                location__region=self.kwargs.get('region_or_customer_type'))

            if region_queryset:
                return region_queryset

            return self.queryset.filter(
                customer_type=self.kwargs.get('region_or_customer_type'))

        return super().get_queryset()
