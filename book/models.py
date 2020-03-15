from enum import Enum

from book.permissions import BookPermissions
from django.contrib.auth.models import User
from django.db import models


class BookStatuses(Enum):
    READ = "read"
    TO_READ = "to_read"

    @classmethod
    def choices(cls):
        return [(cls.READ, "Read"), (cls.TO_READ, "To read")]


class Rates:
    CHOICES = [(i, i) for i in range(1, 10)]


class Author(models.Model):
    name = models.CharField(max_length=50)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    year = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    user = models.ManyToManyField(User, through="UserToBook")
    cover = models.URLField(null=True, blank=True)
    number_of_pages = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("title", "author")
        permissions = ((BookPermissions.MANAGE_BOOKS.codename, "Manage books."),)

    def __str__(self):
        return f"{self.title} - {self.author.name}"


class UserToBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=BookStatuses.choices(), default=BookStatuses.TO_READ
    )
    rate = models.PositiveIntegerField(choices=Rates.CHOICES, null=True, blank=True)
    addition_day = models.DateTimeField(auto_now_add=True)
