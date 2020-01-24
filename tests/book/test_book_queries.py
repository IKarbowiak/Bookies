import graphene
from book.models import Book, UserToBook

BOOKS_QUERY = """
    query Books($author: String, $orderBy: String){
        books(author: $author, orderBy: $orderBy) {
            edges {
            node {
                id
                title
            }
            }
        }
    }
"""


def test_books_query(book, client):
    book2 = Book.objects.get(pk=book.pk)
    book2.pk = None
    book2.title = book.title + " Second part"
    book2.year = book.year - 50
    book2.save()

    variables = {"author": "Sample", "orderBy": "-year"}
    response = client.execute(BOOKS_QUERY, variables=variables)

    result = response["data"]["books"]["edges"]
    assert len(result) == 2
    assert [node["node"]["title"] for node in result] == [book.title, book2.title]


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
            book{
                id
                title
            }
            status
        }
    }
"""


def test_user_book_query(book, user_to_book, client, rq_authenticated):
    user_to_book2 = UserToBook.objects.get(pk=user_to_book.pk)
    user_to_book2.id = None
    user_to_book2.title = "Other book"
    user_to_book2.save()

    response = client.execute(USER_BOOKS_QUERY, context=rq_authenticated)

    data = response["data"]["userBooks"]

    assert len(data) == 2


def test_user_book_query_not_log_in(book, user_to_book, client, rq_anonymous):
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
