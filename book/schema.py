import graphene

from .mutations import AddBook, BookDelete, UserBookDelete


class BookMutation(graphene.ObjectType):
    add_book = AddBook.Field()
    user_book_delete = UserBookDelete.Field()
    book_delete = BookDelete.Field()
