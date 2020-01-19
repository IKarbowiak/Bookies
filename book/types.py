import graphene
from graphene_django.types import DjangoObjectType
from graphene_federation import key

from . import models
from .utils import format_enum_for_display

UserBookStatuses = graphene.Enum.from_enum(models.BookStatuses)


@key(fields="id")
class Author(DjangoObjectType):
    class Meta:
        model = models.Author
        fields = ("name", "id")
        interfaces = (graphene.relay.Node,)


@key(fields="id")
class Book(DjangoObjectType):
    author = graphene.Field(Author, description="The author of the book.")
    description = graphene.String(description="Book desription.")
    cover = graphene.String(description="Url to book cover.")

    class Meta:
        model = models.Book
        fields = ("title", "author", "year", "description", "cover", "id")
        interfaces = (graphene.relay.Node,)

    def resolve_author(root, info, **kwargs):
        return root.author

    def resolve_cover(root, info, **kwargs):
        return root.cover

    def resolve_description(root, info, **kwargs):
        return root.description


@key(fields="id")
class UserToBook(DjangoObjectType):
    book = graphene.Field(Book)
    status = UserBookStatuses()

    class Meta:
        model = models.UserToBook
        fields = ("id", "status", "rate", "book")

    def resolve_book(root, info, **kwargs):
        return root.book

    def resolve_status(root, info, **kwargs):
        return UserBookStatuses.get(format_enum_for_display(root.status))
