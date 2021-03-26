from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
        自定义分页
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
