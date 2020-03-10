from django_filters import CharFilter, FilterSet, NumberFilter, OrderingFilter

from . import models


class BookFilter(FilterSet):
    order_by = OrderingFilter(fields=("title", "year"))
    author = CharFilter(field_name="author__name", lookup_expr="icontains")
    title = CharFilter(field_name="title", lookup_expr="icontains")
    year = NumberFilter(field_name="year")
    year_gte = NumberFilter(field_name="year", lookup_expr="gte")
    year_lte = NumberFilter(field_name="year", lookup_expr="lte")

    class Meta:
        model = models.Book
        fields = ["author", "title", "year", "year_gte", "year_lte"]
