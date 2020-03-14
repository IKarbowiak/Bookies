import graphene
import pytest
from book.models import Author, Book, UserToBook

BOOKS_QUERY = """
    query Books($orderBy: String){
        books(orderBy: $orderBy) {
            edges {
            node {
                id
                title
            }
            }
        }
    }
"""


def test_books_query_order_by_year(book, client):
    book2 = Book.objects.get(pk=book.pk)
    book2.pk = None
    book2.title = book.title + " Second part"
    book2.year = book.year - 50
    book2.save()

    variables = {"orderBy": "-year"}
    response = client.execute(BOOKS_QUERY, variables=variables)

    result = response["data"]["books"]["edges"]
    assert len(result) == 2
    assert [node["node"]["title"] for node in result] == [book.title, book2.title]


def test_books_query_order_by_title(book, client):
    book2 = Book.objects.get(pk=book.pk)
    book2.pk = None
    book2.title = "Book"
    book2.year = book.year - 50
    book2.save()

    variables = {"orderBy": "title"}
    response = client.execute(BOOKS_QUERY, variables=variables)

    result = response["data"]["books"]["edges"]
    assert len(result) == 2
    assert [node["node"]["title"] for node in result] == [book2.title, book.title]


def test_books_query_author_filter(author, book, client):
    query = """
        query Books($author: String){
            books(author: $author) {
                edges {
                    node {
                        id
                        title
                        author {
                            name
                        }
                    }
                }
            }
        }
    """
    author2 = Author.objects.create(name="Example")

    book2 = Book.objects.get(pk=book.pk)
    book2.pk = None
    book2.title = "Book"
    book2.author = author2
    book2.year = book.year - 50
    book2.save()

    variables = {"author": author2.name}
    response = client.execute(query, variables=variables)

    result = response["data"]["books"]["edges"]
    assert len(result) == 1
    assert result[0]["node"]["title"] == book2.title


def test_books_query_title_filter(book, client):
    query = """
        query Books($title: String){
            books(title: $title) {
                edges {
                    node {
                        id
                        title
                    }
                }
            }
        }
    """

    book2 = Book.objects.get(pk=book.pk)
    book2.pk = None
    book2.title = "Book"
    book2.year = book.year - 50
    book2.save()

    variables = {"title": "boo"}
    response = client.execute(query, variables=variables)

    result = response["data"]["books"]["edges"]
    assert len(result) == 2
    assert {node["node"]["title"] for node in result} == {book2.title, book.title}


def test_books_query_year_filter(book, client):
    query = """
        query Books($year: Float){
            books(year: $year) {
                edges {
                    node {
                        id
                        title
                    }
                }
            }
        }
    """
    book2 = Book.objects.get(pk=book.pk)
    book2.pk = None
    book2.title = "Book"
    book2.year = book.year - 50
    book2.save()

    variables = {"year": book.year}
    response = client.execute(query, variables=variables)

    result = response["data"]["books"]["edges"]
    assert len(result) == 1
    assert result[0]["node"]["title"] == book.title


@pytest.mark.parametrize(
    "year_gte, year_lte, count",
    [(1900, None, 2), (1920, None, 1), (1850, 1920, 1), (None, 2000, 2)],
)
def test_books_query_year_gte_and_lte_filter(book, client, year_gte, year_lte, count):
    query = """
        query Books($yearGte: Float, $yearLte: Float){
            books(yearGte: $yearGte, yearLte: $yearLte) {
                edges {
                    node {
                        id
                        title
                    }
                }
            }
        }
    """
    book2 = Book.objects.get(pk=book.pk)
    book2.pk = None
    book2.title = "Book"
    book2.year = book.year + 50
    book2.save()

    variables = {"yearGte": year_gte, "yearLte": year_lte}
    response = client.execute(query, variables=variables)

    result = response["data"]["books"]["edges"]
    assert len(result) == count


BOOK_QUERY = """
    query Book($id: ID!){
        book(id: $id){
            id
            title
            description
            author{
                name
            }
        }
    }
"""


def test_book_query(book, client):
    variables = {"id": graphene.Node.to_global_id("Book", book.pk)}
    response = client.execute(BOOK_QUERY, variables=variables)

    data = response["data"]["book"]

    assert data["title"] == book.title
    assert data["author"]["name"] == book.author.name
    assert data["description"] == book.description


USER_BOOKS_QUERY = """
    query {
        userBooks {
            id
            book{
                id
                title
            }
            status
            rate
        }
    }
"""


def test_user_books_query(book, user_to_book, client, rq_authenticated):
    user_to_book2 = UserToBook.objects.get(pk=user_to_book.pk)
    user_to_book2.id = None
    user_to_book2.title = "Other book"
    user_to_book2.save()

    response = client.execute(USER_BOOKS_QUERY, context=rq_authenticated)

    data = response["data"]["userBooks"]

    assert len(data) == 2


def test_user_books_query_not_log_in(book, user_to_book, client, rq_anonymous):
    user_to_book2 = UserToBook.objects.get(pk=user_to_book.pk)
    user_to_book2.id = None
    user_to_book2.title = "Other book"
    user_to_book2.save()

    response = client.execute(USER_BOOKS_QUERY, context=rq_anonymous)

    assert response["errors"]
    assert (
        response["errors"][0]["message"]
        == "You must be logged in to perform this action."
    )


USER_BOOK_QUERY = """
    query($id: ID!) {
        userBook(id: $id) {
            id
            book{
                id
                title
            }
            status
            rate
        }
    }
"""


def test_user_book_query(user_to_book, client, rq_authenticated):
    book = user_to_book.book
    variables = {"id": graphene.Node.to_global_id("UserToBook", user_to_book.pk)}

    response = client.execute(
        USER_BOOK_QUERY, variables=variables, context=rq_authenticated
    )

    data = response["data"]["userBook"]

    assert data["status"] == user_to_book.status.name.upper()
    assert data["rate"] == user_to_book.rate
    assert data["book"]["title"] == book.title


def test_user_book_query_not_log_in(user_to_book, client, rq_anonymous):
    variables = {"id": graphene.Node.to_global_id("UserToBook", user_to_book.pk)}

    response = client.execute(
        USER_BOOK_QUERY, variables=variables, context=rq_anonymous
    )

    assert response["errors"]
    assert (
        response["errors"][0]["message"]
        == "You must be logged in to perform this action."
    )
