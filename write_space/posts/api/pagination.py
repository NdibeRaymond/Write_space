from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination

class postLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10


class postPageNumberPagination(PageNumberPagination):
    page_size = 5
