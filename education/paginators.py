from rest_framework.pagination import PageNumberPagination


class EducationPaginator(PageNumberPagination):
    """ Пагинатор для вывода информации на странице по 10 записей """

    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 100
