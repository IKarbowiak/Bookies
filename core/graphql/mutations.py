from typing import Tuple

import graphene
from graphene.types.mutation import MutationOptions
from graphql_jwt.exceptions import PermissionDenied


class BaseMutation(graphene.Mutation):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls, permissions: Tuple = None, _meta=None, **options
    ):
        if not _meta:
            _meta = MutationOptions(cls)

        _meta.permissions = permissions
        super().__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def check_permissions(cls, context, permissions):
        if not permissions:
            return True
        if context.user.has_perms(permissions):
            return True
        return False

    @classmethod
    def mutate(cls, root, info, **data):
        if not cls.check_permissions(info.context, cls._meta.permissions):
            raise PermissionDenied()
        return cls.perform_mutation(root, info, **data)

    @classmethod
    def perform_mutation(cls, root, info, **data):
        pass
