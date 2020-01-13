import graphene

from .mutations import AddBookMutation


class BookMutation(graphene.ObjectType):
    add_book = AddBookMutation.Field()
