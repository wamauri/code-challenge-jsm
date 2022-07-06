from rest_framework import serializers
from customers.models import (
    CustomerModel, NameModel, 
    CoordinatesModel, TimezoneModel, 
    LocationModel, PictureModel)


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureModel
        fields = ('large', 'medium', 'thumbnail')


class TimezoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimezoneModel
        fields = ('offset', 'description',)


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoordinatesModel
        fields = ('latitude', 'longitude',)


class LocationSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer(read_only=True)
    timezone = TimezoneSerializer(read_only=True)

    class Meta:
        model = LocationModel
        fields = (
            'region',
            'street',
            'city',
            'state',
            'postcode',
            'coordinates',
            'timezone',
        )


class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameModel
        fields = ('title', 'first', 'last',)


class CustomerSerializer(serializers.ModelSerializer):
    name = NameSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    picture = PictureSerializer(read_only=True)

    class Meta:
        model = CustomerModel
        fields = (
            'customer_type',
            'gender',
            'name',
            'location',
            'email',
            'birthday',
            'registered',
            'telephone_numbers',
            'mobile_numbers',
            'picture',
            'nationality',
        )
