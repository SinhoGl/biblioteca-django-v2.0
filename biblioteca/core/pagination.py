from rest_framework.pagination import LimitOffsetPagination

class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    # You can define your custom upper bound or other settings here
    max_limit = 100  # Example of setting an upper bound