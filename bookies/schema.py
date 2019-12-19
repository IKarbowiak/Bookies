import graphene
import graphql_jwt
from account.schema import AccountMutation, AccountQueries


class Query(AccountQueries, graphene.ObjectType):
    pass


class Mutation(AccountMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
