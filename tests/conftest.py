import pytest
from book.models import Author, Book, BookStatuses, UserToBook
from bookies.schema import schema
from django.contrib.auth.models import AnonymousUser, Permission, User
from django.contrib.sessions.middleware import SessionMiddleware
from graphene.test import Client


@pytest.fixture
def client():
    client = Client(schema)
    return client


@pytest.fixture
def user(db):
    return User.objects.create(username="Test user", password="Test")


@pytest.fixture
def rq_authenticated(rf, user):
    request = rf.post("/")
    SessionMiddleware().process_request(request)
    request.session.save()
    request.user = user

    return request


@pytest.fixture
def rq_anonymous(rf):
    request = rf.post("/")
    SessionMiddleware().process_request(request)
    request.session.save()
    request.user = AnonymousUser()

    return request


@pytest.fixture
def author(db):
    return Author.objects.create(name="Sample author")


@pytest.fixture
def book(author):
    return Book.objects.create(
        title="Sample book",
        author=author,
        year=1900,
        description="Sample description",
        number_of_pages=100,
    )


@pytest.fixture
def user_to_book(user, book):
    return UserToBook.objects.create(
        user=user, book=book, rate=5, status=BookStatuses.READ
    )


@pytest.fixture
def manage_books_permission():
    return Permission.objects.get(codename="manage_books")
