import graphene

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
