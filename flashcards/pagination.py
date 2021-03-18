from rest_framework import pagination
from rest_framework.response import Response


class PagesCountPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        next_page = self.page.next_page_number() if self.page.has_next() else None
        previous_page = self.page.previous_page_number() if self.page.has_previous() else None

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
             },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next_page': next_page,
            'previous_page': previous_page,
            'pages': [x+1 for x in range(self.page.paginator.num_pages)],
            'results': data
        })

class PagesCountSmallPagination(PagesCountPagination):
    page_size = 20
