from customers.views import change_dataframe, create_customers
from rest_framework.test import APIClient
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
import pandas as pd
import json
import os


class APIViewsTest(TestCase):
    def setUp(self) -> None:
        self.path = os.path.join(settings.BASE_DIR, 'tests')
        self.client = APIClient()
        with open(f'{self.path}/utils/input-backend.csv', 'r') as file:
            self.file = file
            self.main_df = pd.read_csv(self.file)
            file.close()
        self.localhost = 'http://127.0.0.1:8000/'

    def tearDown(self) -> None:
        pass

    def test_api_list_view(self):
        url = reverse('customers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_api_list_view_filter_by_region_and_customer_type(self):
        final_datafame = change_dataframe(self.main_df)
        create_customers(final_datafame)
        url = f'{self.localhost}api/v1/customers/norte/laborious/'
        response = self.client.get(url)
        data = json.dumps(response.data)
        customer_type = json.loads(data)['results'][0]['customer_type']
        customer_region = json.loads(data)['results'][0]['location']['region']

        self.assertEqual(customer_type, 'laborious')
        self.assertEqual(customer_region, 'norte')

    def test_api_list_view_filter_by_region(self):
        final_datafame = change_dataframe(self.main_df)
        create_customers(final_datafame)
        url = f'{self.localhost}api/v1/customers/nordeste/'
        response = self.client.get(url)
        data = json.dumps(response.data)
        customer_region = json.loads(data)['results'][0]['location']['region']

        self.assertEqual(customer_region, 'nordeste')

    def test_api_list_view_filter_by_customer_type(self):
        final_datafame = change_dataframe(self.main_df)
        create_customers(final_datafame)
        url = f'{self.localhost}api/v1/customers/special/'
        response = self.client.get(url)
        data = json.dumps(response.data)
        customer_type = json.loads(data)['results'][0]['customer_type']

        self.assertEqual(customer_type, 'special')
