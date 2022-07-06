from django.core.validators import validate_email
from django.db import models


class NameModel(models.Model):
    title = models.CharField('Title', max_length=5)
    first = models.CharField('First', max_length=50)
    last = models.CharField('Last', max_length=50)

    class Meta:
        verbose_name = 'Name'
        verbose_name_plural = 'Names'
        ordering = ['id']

    def __str__(self) -> str:
        return self.first


class CoordinatesModel(models.Model):
    latitude = models.CharField('Latitude', max_length=21)
    longitude = models.CharField('longitude', max_length=21)

    class Meta:
        verbose_name = 'Coordinates'
        verbose_name_plural = 'Coordinates'
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.latitude} {self.longitude}'


class TimezoneModel(models.Model):
    offset = models.CharField('Offset', max_length=8)
    description = models.CharField('Description', max_length=150)

    class Meta:
        verbose_name = 'Timezone'
        verbose_name_plural = 'Time Zones'
        ordering = ['id']

    def __str__(self) -> str:
        return self.offset


class LocationModel(models.Model):
    region = models.CharField('Region', max_length=15)
    street = models.CharField('Street', max_length=50)
    city = models.CharField('City', max_length=50)
    state = models.CharField('State', max_length=30)
    postcode = models.IntegerField('Postcode')

    coordinates = models.ForeignKey(
        CoordinatesModel, on_delete=models.CASCADE, 
        related_name='location_model')

    timezone = models.ForeignKey(
        TimezoneModel, on_delete=models.CASCADE, 
        related_name='location_model')

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ['id']

    def __str__(self) -> str:
        return self.region


class PictureModel(models.Model):
    large = models.URLField('Large', max_length=255)
    medium = models.URLField('Medium', max_length=255)
    thumbnail = models.URLField('Thumbnail', max_length=255)

    class Meta:
        verbose_name = 'Picture'
        verbose_name_plural = 'Pictures'
        ordering = ['id']

    def __str__(self) -> str:
        return str(self.large)


class CustomerModel(models.Model):
    customer_type = models.CharField('Type', max_length=50)

    gender = models.CharField('Gender', max_length=1)

    name = models.ForeignKey(
        NameModel, on_delete=models.CASCADE, related_name='customer_model'
    )

    location = models.ForeignKey(
        LocationModel, on_delete=models.CASCADE, related_name='customer_model'
    )

    email = models.EmailField(
        'E-mail', max_length=50, validators=[validate_email])

    birthday = models.CharField('Birthday', max_length=50)

    registered = models.CharField('Registered', max_length=50)

    telephone_numbers = models.JSONField(
        default=list, verbose_name='Telephone Numbers'
    )

    mobile_numbers = models.JSONField(
        default=list, verbose_name='Mobile Numbers'
    )

    picture = models.ForeignKey(
        PictureModel, on_delete=models.CASCADE, related_name='customer_model'
    )

    nationality = models.CharField('Nationality', max_length=2, default='BR')

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['id']

    def __str__(self) -> str:
        return str(self.email)
