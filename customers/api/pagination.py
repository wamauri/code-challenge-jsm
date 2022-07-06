from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 5
    max_page_size = 50

    def get_paginated_response(self, data):
        response = dict()

        response['pageNumber'] = self.page.number
        response['pageSize'] = self.page_size
        response['totalCount'] = self.page.paginator.count
        response['users'] = [str(self.request.user)]
        response['results'] = data

        return Response(response)
