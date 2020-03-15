import graphene
import graphql_jwt
from account.graphql.schema import AccountMutation, AccountQueries
from book.graphql.schema import BookMutation, BookQueries


class Query(AccountQueries, BookQueries, graphene.ObjectType):
    pass


class Mutation(AccountMutation, BookMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
