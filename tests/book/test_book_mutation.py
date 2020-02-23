import graphene
from book.models import BookStatuses

BOOK_DELETE_MUTATION = """
    mutation BookDelete($id: ID!){
            bookDelete(id: $id){
                book{
                    id
                    title
                    author{
                        name
                    }
                    description
                    cover
                }
            }
        }
"""


def test_delete_book_mutation(book, client):
    variables = {"id": graphene.Node.to_global_id("Book", book.pk)}
    response = client.execute(BOOK_DELETE_MUTATION, variables=variables)

    data = response["data"]["bookDelete"]["book"]

    assert data["title"] == book.title
    assert data["author"]["name"] == book.author.name


USER_BOOK_DELETE_MUTATION = """
    mutation UserBookDelete($id: ID!){
            userBookDelete(id: $id){
                userBook{
                    status
                    rate
                    book{
                        title
                        author{
                            name
                        }
                        description
                        cover
                    }
                }
            }
        }
"""


def test_delete_user_book_mutation(user_to_book, rq_authenticated, client):
    book = user_to_book.book

    variables = {"id": graphene.Node.to_global_id("UserToBook", user_to_book.pk)}
    response = client.execute(
        USER_BOOK_DELETE_MUTATION, variables=variables, context=rq_authenticated
    )

    data = response["data"]["userBookDelete"]["userBook"]

    assert data["book"]["title"] == book.title
    assert data["book"]["author"]["name"] == book.author.name
    assert data["status"] == user_to_book.status.name


USER_BOOK_UPDATE_MUTATION = """
    mutation UserBookUpdate($id: ID!, $status: BookStatuses!, $rate: Int!){
            userBookUpdate(id: $id, status: $status, rate: $rate){
                userBook{
                    status
                    rate
                    book{
                        title
                        author{
                            name
                        }
                        description
                        cover
                    }
                }
            }
        }
"""


def test_user_book_update_mutation(user_to_book, rq_authenticated, client):
    book = user_to_book.book

    new_status = BookStatuses.READ.name
    rate = 6

    assert user_to_book.rate != rate
    assert user_to_book.status != new_status

    variables = {
        "id": graphene.Node.to_global_id("UserToBook", user_to_book.pk),
        "status": new_status,
        "rate": rate,
    }
    response = client.execute(
        USER_BOOK_UPDATE_MUTATION, variables=variables, context=rq_authenticated
    )

    user_to_book.refresh_from_db()
    data = response["data"]["userBookUpdate"]["userBook"]
    assert data["book"]["title"] == book.title
    assert data["book"]["author"]["name"] == book.author.name
    assert data["status"] == new_status.upper() == user_to_book.status.upper()
    assert data["rate"] == rate == user_to_book.rate


def test_user_book_update_mutation_wrong_rate(user_to_book, rq_authenticated, client):
    new_status = BookStatuses.READ.name
    rate = 11

    assert user_to_book.rate != rate
    assert user_to_book.status != new_status

    variables = {
        "id": graphene.Node.to_global_id("UserToBook", user_to_book.pk),
        "status": new_status,
        "rate": rate,
    }
    response = client.execute(
        USER_BOOK_UPDATE_MUTATION, variables=variables, context=rq_authenticated
    )

    user_to_book.refresh_from_db()
    errors = response["errors"]
    assert errors
    assert errors[0]["message"] == "Rate value must be between 1 and 10"
