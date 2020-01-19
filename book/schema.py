import graphene
from graphene_django.filter import DjangoFilterConnectionField

from . import models
from .filters import BookFilter
from .mutations import AddBook, BookDelete, UserBookDelete
from .types import Book


class BookMutation(graphene.ObjectType):
    add_book = AddBook.Field()
    user_book_delete = UserBookDelete.Field()
    book_delete = BookDelete.Field()


class BookQueries(graphene.ObjectType):
    book = graphene.Field(
        Book,
        id=graphene.Argument(graphene.ID, description="ID of book.", required=True),
        description="Look up a book by ID",
    )
    books = DjangoFilterConnectionField(Book, filterset_class=BookFilter)

    def resolve_books(self, info, **kwargs):
        return models.Book.objects.all()

    def resolve_book(self, info, id, **kwargs):
        _, pk = graphene.Node.from_global_id(id)
        return models.Book.objects.get(pk=pk)