from django.contrib import admin
from .models import (
    NameModel, CoordinatesModel, 
    TimezoneModel, LocationModel, 
    PictureModel, CustomerModel)


@admin.register(NameModel)
class NameModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'title', 
        'first',
        'last',)


@admin.register(CoordinatesModel)
class CoordinatesModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'latitude', 
        'longitude',)


@admin.register(TimezoneModel)
class TimezoneModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'offset', 
        'description',)


@admin.register(LocationModel)
class LocationModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'region', 
        'street', 
        'city', 
        'state', 
        'postcode', 
        'coordinates',
        'timezone',)


@admin.register(PictureModel)
class PictureModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'large', 
        'medium', 
        'thumbnail',)


@admin.register(CustomerModel)
class CatalogoModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
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
        'nationality',)
