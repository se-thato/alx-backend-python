from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response


class CustomCursorPagination(CursorPagination):
    """
    Custom pagination class that uses cursor-based pagination.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = 'id'


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class that uses page number based pagination.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'results': data,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        })