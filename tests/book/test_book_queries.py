import graphene
from book.models import Book

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
