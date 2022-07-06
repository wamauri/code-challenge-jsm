from django.test import TestCase
from model_mommy import mommy


class ModelsTest(TestCase):

    def setUp(self) -> None:
        self.name = mommy.make('NameModel')
        self.coordinates = mommy.make('CoordinatesModel')
        self.timezone = mommy.make('TimezoneModel')
        self.location = mommy.make('LocationModel')
        self.picture = mommy.make('PictureModel')
        self.customer = mommy.make('CustomerModel')

    def tearDown(self) -> None:
        return super().tearDown()

    def test_name_model_str_method(self):
        self.assertEqual(str(self.name), self.name.first)

    def test_coordinates_model_str_method(self):
        self.assertEqual(
            str(self.coordinates), 
            f'{self.coordinates.latitude} {self.coordinates.longitude}')

    def test_timezone_model_str_method(self):
        self.assertEqual(str(self.timezone), self.timezone.offset)

    def test_location_model_str_method(self):
        self.assertEqual(str(self.location), self.location.region)

    def test_picture_model_str_method(self):
        self.assertEqual(str(self.picture), self.picture.large)

    def test_customer_model_str_method(self):
        self.assertEqual(str(self.customer), self.customer.email)
