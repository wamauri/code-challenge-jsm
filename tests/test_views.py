from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import RequestFactory
from django.test import TestCase, Client
from django.conf import settings
import pandas as pd
import os
from customers.models import (
    NameModel, CoordinatesModel, 
    TimezoneModel, LocationModel,
    PictureModel, CustomerModel)
from customers.views import (
    get_region, get_customer_type, change_gender_name_format,
    change_phonenumber_format, change_dataframe, prepare_name,
    prepare_coordinates, prepare_timezone, prepare_location,
    prepare_picture, prepare_customer, json_to_dataframe,
    create_customers, create_customers_from_csv_url,
    create_customers_from_json_url, create_customers_from_csv_file,
    create_customers_from_json_file, load_json_or_csv
)


class ViewsTest(TestCase):

    def setUp(self) -> None:
        self.path = os.path.join(settings.BASE_DIR, 'tests')

        with open(f'{self.path}/utils/input-backend.csv', 'r') as file:
            self.file = file
            self.main_df = pd.read_csv(self.file)
            file.close()

        self.state = 'bahia'
        self.region = 'nordeste'
        self.csv_url = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv'
        self.json_url = 'https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json'
        # CSRF_TOKEN
        client = Client(enforce_csrf_checks=True)
        client.get('http://127.0.0.1:8000/')
        self.csrf_token = client.cookies['csrftoken'].value
        self.factory = RequestFactory()
        self.localhost = 'http://127.0.0.1:8000/'
        self.img = 'https://www.elegantthemes.com/blog/wp-content/uploads/2015/02/custom-trackable-short-url-feature.png'

    def tearDown(self) -> None:
        pass

    def test_get_region(self):
        region = get_region(self.state)
        self.assertEqual(region, self.region)

    def test_get_customer_type_special(self):
        customer_type = get_customer_type(-34.276939, -2.196999)
        self.assertEqual(customer_type, 'special')

    def test_get_customer_type_normal(self):
        customer_type = get_customer_type(-46.603599, -26.155682)
        self.assertEqual(customer_type, 'normal')

    def test_get_customer_type_laborious(self):
        customer_type = get_customer_type(-34.276937, -2.196997)
        self.assertEqual(customer_type, 'laborious')

    def test_change_gender_name(self):
        gender = change_gender_name_format('male')
        self.assertEqual(gender, 'M')

    def test_change_phonenumber_format(self):
        phonenumber = change_phonenumber_format('(75)99966-9966')
        self.assertEqual(phonenumber, '+5575999669966')

    def test_change_dataframe(self):
        new_df = change_dataframe(self.main_df)
        self.assertEqual(new_df['gender'][0], 'F')

    def test_prepare_name(self):
        name = prepare_name(self.main_df)
        instance = next(name)
        self.assertIsInstance(instance, NameModel)

    def test_prepare_coordinates(self):
        coordinates = prepare_coordinates(self.main_df)
        instance = next(coordinates)
        self.assertIsInstance(instance, CoordinatesModel)

    def test_prepare_timezone(self):
        timezone = prepare_timezone(self.main_df)
        instance = next(timezone)
        self.assertIsInstance(instance, TimezoneModel)

    def test_prepare_location(self):
        coordinates = prepare_coordinates(self.main_df)
        timezone = prepare_timezone(self.main_df)
        location = prepare_location(self.main_df, coordinates, timezone)
        instance = next(location)
        self.assertIsInstance(instance, LocationModel)

    def test_prepare_picture(self):
        picture = prepare_picture(self.main_df)
        instance = next(picture)
        self.assertIsInstance(instance, PictureModel)

    def test_prepare_customer(self):
        name = prepare_name(self.main_df)
        coordinates = prepare_coordinates(self.main_df)
        picture = prepare_picture(self.main_df)
        timezone = prepare_timezone(self.main_df)
        location = prepare_location(self.main_df, coordinates, timezone)
        customer = prepare_customer(self.main_df, name, location, picture)
        instance = next(customer)
        self.assertIsInstance(instance, CustomerModel)

    def test_json_to_dataframe(self):
        df = pd.read_json(self.json_url)
        dataframe = json_to_dataframe(df)
        self.assertIsInstance(dataframe, pd.DataFrame)

    def test_create_customers(self):
        final_datafame = change_dataframe(self.main_df)
        res = create_customers(final_datafame)
        self.assertIsNone(res)

    def test_create_customers_from_csv_url(self):
        res = create_customers_from_csv_url(self.csv_url)
        self.assertIsNone(res)

    def test_create_customers_from_json_url(self):
        res = create_customers_from_json_url(self.json_url)
        self.assertIsNone(res)

    def test_create_customers_from_csv_file(self):
        data = dict()
        data['csrf_token'] = self.csrf_token
        data['url'] = ''
        with open(f'{self.path}/utils/input-backend.csv', 'rb') as file:
            self.file = file.read()
            csv = SimpleUploadedFile(
                name='input-backend.csv', 
                content=self.file, 
                content_type='multipart/form-data'
            )
            data['file'] = csv
            resquest = self.factory.post(
                path=self.localhost, 
                data=data,
            )
            res = create_customers_from_csv_file(resquest)
            self.assertIsNone(res)

    def test_create_customers_from_json_file(self):
        data = dict()
        data['csrf_token'] = self.csrf_token
        data['url'] = ''
        with open(f'{self.path}/utils/input-backend.json', 'rb') as file:
            self.file = file.read()
            json = SimpleUploadedFile(
                name='input-backend.json', 
                content=self.file, 
                content_type='multipart/form-data'
            )
            data['file'] = json
            resquest = self.factory.post(
                path=self.localhost, 
                data=data,
            )
            res = create_customers_from_json_file(resquest)
            self.assertIsNone(res)

    def test_load_json_or_csv_from_json_url(self):
        data = dict()
        data['csrf_token'] = self.csrf_token
        data['url'] = self.json_url

        request = self.factory.post(
            path=self.localhost, 
            data=data
        )
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        res = load_json_or_csv(request)
        self.assertEqual(res.status_code, 200)

    def test_load_json_or_csv_from_csv_url(self):
        data = dict()
        data['csrf_token'] = self.csrf_token
        data['url'] = self.csv_url

        request = self.factory.post(
            path=self.localhost, 
            data=data
        )
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        res = load_json_or_csv(request)
        self.assertEqual(res.status_code, 200)

    def test_load_json_or_csv_from_csv_file(self):
        data = dict()
        data['csrf_token'] = self.csrf_token
        data['url'] = ''
        with open(f'{self.path}/utils/input-backend.csv', 'rb') as file:
            self.file = file.read()
            csv = SimpleUploadedFile(
                name='input-backend.csv', 
                content=self.file, 
                content_type='multipart/form-data'
            )
            data['file'] = csv
            request = self.factory.post(
                path=self.localhost, 
                data=data,
            )
            setattr(request, 'session', 'session')
            messages = FallbackStorage(request)
            setattr(request, '_messages', messages)
            res = load_json_or_csv(request)
            self.assertEqual(res.status_code, 200)

    def test_load_json_or_csv_from_json_file(self):
        data = dict()
        data['csrf_token'] = self.csrf_token
        data['url'] = ''
        with open(f'{self.path}/utils/input-backend.json', 'rb') as file:
            self.file = file.read()
            json = SimpleUploadedFile(
                name='input-backend.json', 
                content=self.file, 
                content_type='multipart/form-data'
            )
            data['file'] = json
            request = self.factory.post(
                path=self.localhost, 
                data=data,
            )
            setattr(request, 'session', 'session')
            messages = FallbackStorage(request)
            setattr(request, '_messages', messages)
            res = load_json_or_csv(request)
            self.assertEqual(res.status_code, 200)

    def test_load_json_or_csv_from_image_url(self):
            data = dict()
            data['csrf_token'] = self.csrf_token
            data['url'] = self.img

            request = self.factory.post(
                path=self.localhost, 
                data=data
            )
            setattr(request, 'session', 'session')
            messages = FallbackStorage(request)
            setattr(request, '_messages', messages)
            res = load_json_or_csv(request)
            self.assertEqual(res.status_code, 200)

    def test_load_json_or_csv_from_png_file(self):
            data = dict()
            data['csrf_token'] = self.csrf_token
            data['url'] = ''
            with open(f'{self.path}/utils/img.png', 'rb') as file:
                self.file = file.read()
                png = SimpleUploadedFile(
                    name='img.png', 
                    content=self.file, 
                    content_type='multipart/form-data'
                )
                data['file'] = png
                request = self.factory.post(
                    path=self.localhost, 
                    data=data,
                )
                setattr(request, 'session', 'session')
                messages = FallbackStorage(request)
                setattr(request, '_messages', messages)
                res = load_json_or_csv(request)
                self.assertEqual(res.status_code, 200)

    def test_load_json_or_csv_from_without_url(self):
            data = dict()
            data['csrf_token'] = self.csrf_token
            data['url'] = ''

            request = self.factory.post(
                path=self.localhost, 
                data=data
            )
            setattr(request, 'session', 'session')
            messages = FallbackStorage(request)
            setattr(request, '_messages', messages)
            res = load_json_or_csv(request)
            self.assertEqual(res.status_code, 200)
