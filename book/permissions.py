from enum import Enum


class BasePermissionEnum(Enum):
    @property
    def codename(self):
        return self.value.split(".")[1]


class BookPermissions(BasePermissionEnum):
    MANAGE_BOOKS = "book.manage_books"
