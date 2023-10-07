from rest_framework.pagination import PageNumberPagination


class EducationPaginator(PageNumberPagination):
    """ Пагинатор для вывода информации на странице по 10 записей """

    page_size = 10
