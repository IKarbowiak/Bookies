from django.contrib.auth.models import User
from django.db import models


class BookStatuses:
    READ = "read"
    TO_READ = "to_read"

    CHOICES = [(READ, "Read"), (TO_READ, "To read")]


class Rates:
    CHOICES = [(i, i) for i in range(10)]


class Author(models.Model):
    name = models.CharField(max_length=50)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    user = models.ManyToManyField(User, through="UserToBook")


class UserToBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=BookStatuses.CHOICES)
    rate = models.PositiveIntegerField(choices=Rates.CHOICES, null=True, blank=True)
    addition_day = models.DateTimeField(auto_now_add=True)
