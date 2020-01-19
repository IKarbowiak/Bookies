from django_filters import CharFilter, FilterSet, OrderingFilter

from . import models


def search_author(qs, _, value):
    if value:
        return qs.filter(author__name__icontains=value)
    return qs


# TODO: allow to filter with icontains, not only exact
class BookFilter(FilterSet):
    order_by = OrderingFilter(fields=("title", "year"))
    author = CharFilter(method=search_author)

    class Meta:
        model = models.Book
        fields = ["title", "year", "author"]
