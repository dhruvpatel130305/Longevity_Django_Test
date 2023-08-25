from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Create custom pagination for list APIs
    """
    page_size_query_param = 'page_size'