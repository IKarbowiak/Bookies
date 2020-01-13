import graphene
import graphql_jwt
from account.schema import AccountMutation, AccountQueries
from book.schema import BookMutation


class Query(AccountQueries, graphene.ObjectType):
    pass


class Mutation(AccountMutation, BookMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
