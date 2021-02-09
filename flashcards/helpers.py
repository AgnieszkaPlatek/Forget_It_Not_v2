from rest_framework import filters


class CardFrontBackSearchFilter(filters.SearchFilter):
    """
    Enables the user to specify search fields and if none are chosen both fields are used.
    """
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', ['front', 'back'])
