import graphene
from graphene_django.filter import DjangoFilterConnectionField

from . import models
from .filters import BookFilter
from .mutations import AddBook, BookDelete, UserBookDelete, UserBookUpdate
from .types import Book, UserToBook


class BookMutation(graphene.ObjectType):
    add_book = AddBook.Field()
    user_book_delete = UserBookDelete.Field()
    user_book_update = UserBookUpdate.Field()
    book_delete = BookDelete.Field()


class BookQueries(graphene.ObjectType):
    book = graphene.Field(
        Book,
        id=graphene.Argument(graphene.ID, description="ID of book.", required=True),
        description="Look up a book by ID.",
    )
    books = DjangoFilterConnectionField(Book, filterset_class=BookFilter)
    user_book = graphene.Field(
        UserToBook,
        id=graphene.ID(graphene.ID, description="ID of user book.", required=True),
        description="Look up a user book by ID.",
    )
    user_books = graphene.List(UserToBook, description="List of user books.")

    def resolve_books(self, info, **kwargs):
        return models.Book.objects.all()

    def resolve_book(self, info, id, **kwargs):
        _, pk = graphene.Node.from_global_id(id)
        return models.Book.objects.get(pk=pk)

    def resolve_user_book(self, info, id, **kwargs):
        _, pk = graphene.Node.from_global_id(id)
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to perform this action.")
        return models.UserToBook.objects.get(pk=pk, user=user)

    def resolve_user_books(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to perform this action.")
        return models.UserToBook.objects.filter(user=user)
