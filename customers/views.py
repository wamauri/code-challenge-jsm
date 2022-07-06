from .utils.states_by_region import regions
from typing import Type, Generator, List
from django.contrib import messages
from django.shortcuts import render
import pandas as pd
import re
from .models import (
    CustomerModel, PictureModel,
    LocationModel, TimezoneModel,
    CoordinatesModel, NameModel
)


def get_columns(main_dict: dict) -> Generator:
    '''Gets dict keys and converts to columns'''
    for fisrt_key, fisrt_value in main_dict.items():
        if not isinstance(fisrt_value, dict):

            yield fisrt_key

        if isinstance(fisrt_value, dict):
            for second_key, second_value in fisrt_value.items():
                if not isinstance(second_value, dict):

                    yield fisrt_key +'__'+ second_key

                if isinstance(second_value, dict):
                    for third_key in second_value.keys():

                        yield fisrt_key +'__'+ second_key +'__'+ third_key


def get_cells(main_dict: dict) -> Generator:
    '''Gets dict values and organize, 
    it must be converted in list on function call.
    '''
    for _, fisrt_value in main_dict.items():
        if not isinstance(fisrt_value, dict):

            yield fisrt_value

        if isinstance(fisrt_value, dict):

            for _, second_value in fisrt_value.items():
                if not isinstance(second_value, dict):

                    yield second_value
                else:
                    for _, third_value in second_value.items():

                        yield third_value


def json_to_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    '''Converts json to pandas dataframe '''
    count = 0
    df_from_json = pd.DataFrame()

    for my_dict in dataframe['results']:

        if count == 0:
            columns = list(get_columns(my_dict))
            for column in columns:
                df_from_json[column] = column

        # Add a new values row to df_from_json dataframe
        df_from_json.loc[len(df_from_json.index)] = list(get_cells(my_dict))
        count += 1

    return df_from_json


def get_region(state: str):

    for key, values in regions.items():
            for value in values:
                if value == state:
                    return key


def get_customer_type(latitude: float, longitude: float) -> str:
    '''Checks if customer type is special, normal or laborious 
    by his coordinates latitude and longitude.
    '''
    if 34.276938 <= abs(latitude) <= 52.997614 \
        and 2.196998 <= abs(longitude) <= 23.966413:

        return 'special'

    elif 46.603598 <= abs(latitude) <= 54.777426 \
        and 26.155681 <= abs(longitude) <= 34.016466:

        return 'normal'

    else:
        return 'laborious'


def change_gender_name_format(text: str) -> str:
    '''Gets the first letter of a word and 
    change letter to uppercase.
    '''

    return text[:1].upper()


def change_phonenumber_format(phonenumber: str) -> str:
    '''Gets only digits in a string and 
    add +55 for the E.164 format.
    '''

    return '+55' + re.sub('[^0-9]', '', phonenumber)


def edit_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    '''Changes the information as asked in description of code challenge'''
    dataframe['gender'] = dataframe['gender'].apply(change_gender_name_format)
    dataframe['phone'] = dataframe['phone'].apply(change_phonenumber_format)
    dataframe['cell'] = dataframe['cell'].apply(change_phonenumber_format)

    return dataframe


def exclude_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    '''Exclude dob__age and registered__age colummns'''
    dataframe.drop(columns="dob__age", axis=1, inplace=True)
    dataframe.drop(columns="registered__age", axis=1, inplace=True)

    return dataframe


def change_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = edit_columns(dataframe)

    return exclude_columns(dataframe)


def prepare_name(final_dataframe: pd.DataFrame) -> Generator:
    for row in final_dataframe.itertuples():

        yield NameModel(
            title=row.name__title,
            first=row.name__first,
            last=row.name__last
        )


def prepare_coordinates(final_dataframe: pd.DataFrame) -> Generator:
    for row in final_dataframe.itertuples():

        yield CoordinatesModel(
            latitude=row.location__coordinates__latitude,
            longitude=row.location__coordinates__longitude
        )


def prepare_timezone(final_dataframe: pd.DataFrame) -> Generator:
    for row in final_dataframe.itertuples():

        yield TimezoneModel(
            offset=row.location__timezone__offset,
            description=row.location__timezone__description
        )


def prepare_location(
    final_dataframe: pd.DataFrame, 
    coordinates: List[Type[CoordinatesModel]], 
    timezones: List[Type[TimezoneModel]]) -> Generator:

    for row, coordinate, timezone in zip(
        final_dataframe.itertuples(), 
        coordinates, 
        timezones
    ):

        yield LocationModel(
            region=get_region(row.location__state),
            street=row.location__street,
            city=row.location__city,
            state=row.location__state,
            postcode=row.location__postcode,
            coordinates_id=coordinate.id,
            timezone_id=timezone.id
        )


def prepare_picture(final_dataframe: pd.DataFrame) -> Generator:
    for row in final_dataframe.itertuples():

        yield PictureModel(
            large=row.picture__large,
            medium=row.picture__medium,
            thumbnail=row.picture__thumbnail
        )


def prepare_customer(
    final_dataframe: pd.DataFrame,
    names: List[Type[NameModel]],
    locations: List[Type[LocationModel]],
    pictures: List[Type[PictureModel]]) -> Generator:

    for row, name, location, picture in zip(
        final_dataframe.itertuples(), names, 
        locations, pictures
    ):

        yield CustomerModel(
            customer_type=get_customer_type(
                float(row.location__coordinates__latitude),
                float(row.location__coordinates__longitude)
            ),
            gender=row.gender,
            name_id=name.id,
            location_id=location.id,
            email=row.email,
            birthday=row.dob__date,
            registered=row.registered__date,
            telephone_numbers=[row.phone],
            mobile_numbers=[row.cell],
            picture_id=picture.id
        )


def create_customers(final_datafame) -> None:

    names_to_create = list(prepare_name(final_dataframe=final_datafame))
    names = NameModel.objects.bulk_create(names_to_create)

    coordinates_to_create = list(
        prepare_coordinates(final_dataframe=final_datafame)
    )
    coordinates = CoordinatesModel.objects.bulk_create(coordinates_to_create)

    timezone_to_create = list(
        prepare_timezone(final_dataframe=final_datafame)
    )
    timezones = TimezoneModel.objects.bulk_create(timezone_to_create)

    picture_to_create = list(prepare_picture(final_dataframe=final_datafame))
    pictures = PictureModel.objects.bulk_create(picture_to_create)

    location_to_create = list(
        prepare_location(
            final_dataframe=final_datafame,
            coordinates=coordinates,
            timezones=timezones
        )
    )
    locations = LocationModel.objects.bulk_create(location_to_create)

    customer_to_create = list(
        prepare_customer(
            final_dataframe=final_datafame,
            names=names,
            locations=locations,
            pictures=pictures
        )
    )
    CustomerModel.objects.bulk_create(customer_to_create)


def create_customers_from_csv_url(url: str) -> None:
    df = pd.read_csv(url)
    final_datafame = change_dataframe(df)
    create_customers(final_datafame)


def create_customers_from_csv_file(request) -> None:
    csv_file = request.FILES['file']
    df = pd.read_csv(csv_file)
    final_datafame = change_dataframe(df)
    create_customers(final_datafame)


def create_customers_from_json_url(url: str) -> None:
    df = pd.read_json(url)
    new_df = json_to_dataframe(df)
    final_datafame = change_dataframe(new_df)
    create_customers(final_datafame)


def create_customers_from_json_file(request) -> None:
    json = request.FILES['file']
    df = pd.read_json(json)
    new_df = json_to_dataframe(df)
    final_datafame = change_dataframe(new_df)
    create_customers(final_datafame)


def load_json_or_csv(request):

    if request.method == 'POST':

        if bool(request.POST['url']) != False:
            url = request.POST['url']

            if url.split('.')[-1] == 'csv':
                create_customers_from_csv_url(url=url)
                messages.success(
                    request, 'Carregamento do CSV realizado com sucesso'
                )

            elif url.split('.')[-1] == 'json':
                create_customers_from_json_url(url=url)
                messages.success(
                    request, 'Carregamento do JSON realizado com sucesso'
                )
            else:
                messages.warning(
                    request, 'O link precisa ser json ou csv')

        elif bool(request.FILES) != False:
            file = request.FILES['file']

            if file.name.endswith('.csv'):
                create_customers_from_csv_file(request)
                messages.success(
                    request, 'Carregamento do CSV realizado com sucesso'
                )

            elif file.name.endswith('.json'):
                create_customers_from_json_file(request)
                messages.success(
                    request, 'Carregamento do JSON realizado com sucesso'
                )
            else:
                messages.error(
                    request, 'Faça o upload de um arquivo json ou csv.')
        else:
            messages.warning(request, 'O campo não pode estar vazio')

    return render(request, 'index.html')
