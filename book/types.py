import graphene
from graphene_django.types import DjangoObjectType

from . import models

UserBookStatuses = graphene.Enum.from_enum(models.BookStatuses)


class Author(DjangoObjectType):
    class Meta:
        model = models.Author
        fields = ("name",)


class Book(DjangoObjectType):
    author = graphene.Field(Author, description="The author of the book.")
    description = graphene.String(description="Book desription.")
    cover = graphene.String(description="Url to book cover.")

    class Meta:
        model = models.Book
        fields = ("title", "author", "year", "description", "cover")

    def resolve_author(root, info, **kwargs):
        return root.author

    def resolve_cover(root, info, **kwargs):
        return root.cover.url if root.cover else ""

    def resolve_description(root, info, **kwargs):
        return root.description
