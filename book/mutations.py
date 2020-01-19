import graphene
from django.core.exceptions import ObjectDoesNotExist

from . import models
from .types import Book, UserBookStatuses, UserToBook
from .utils import book_get_or_create


class AddBook(graphene.Mutation):
    book = graphene.Field(Book)

    class Arguments:
        title = graphene.String(description="Title of the book.", required=True)
        author = graphene.String(description="Author of the book.", required=True)
        status = graphene.Argument(
            UserBookStatuses,
            description="Information if book is already read or not.",
            required=True,
        )
        rate = graphene.Int(description="Rate of the book.", required=False)

    @classmethod
    def mutate(cls, root, info, title, author, status, **data):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to perform this action.")

        rate = data.get("rate")
        if rate:
            cls.validate_rate(rate)

        book = book_get_or_create(title, author)

        user_book, created = models.UserToBook.objects.get_or_create(
            user=user, book=book
        )
        if not created:
            raise Exception("This book is added to this user already.")
        user_book.status = status
        user_book.rate = rate if rate else None
        user_book.save()

        return AddBook(book)

    @staticmethod
    def validate_rate(rate):
        try:
            rate = int(rate)
        except ValueError:
            raise Exception("Rate must mu number value.")
        if rate < 1 or rate > 10:
            raise Exception("Rate value must be between 1 and 10")


class BookDelete(graphene.Mutation):
    book = graphene.Field(Book)

    class Arguments:
        id = graphene.ID(description="ID of book to delete.", required=True)

    @classmethod
    def mutate(cls, root, info, id, **data):
        only_type, pk = graphene.Node.from_global_id(id)
        try:
            book = models.Book.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Exception(f"Book with id {id} does not exists.")
        book.delete()
        return BookDelete(book)


class UserBookDelete(graphene.Mutation):
    user_book = graphene.Field(UserToBook)

    class Arguments:
        id = graphene.ID(description="ID of user book to delete.", required=True)

    @classmethod
    def mutate(cls, root, info, id, **data):
        # TODO: create base mutation and move this checking there
        only_type, pk = graphene.Node.from_global_id(id)
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to perform this action.")
        try:
            user_book = models.UserToBook.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Exception(f"User book with id {id} does not exists.")
        user_book.delete()
        return UserBookDelete(user_book)
