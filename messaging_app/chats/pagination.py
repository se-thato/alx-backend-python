from rest_framework.pagination import CursorPagination


class CursorPagination(CursorPagination):
    """
    Custom pagination class that uses cursor-based pagination.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20
    ordering = 'id'