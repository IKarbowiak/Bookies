import json
import ssl
import urllib

from book.models import Author, Book
from django.conf import settings


# there are more info in goodread like rating and author photos
def book_get_or_create(title: str, author: str) -> Book:
    book = Book.objects.filter(title=title, author__name=author).first()
    if book:
        return Book

    book_data = get_book_details(title, author)

    title = book_data["title"]
    author = book_data["authors"][0]
    image_data = book_data.get("imageLinks")
    cover_url = image_data.get("thumbnail") if image_data else None
    publication_year = book_data.get("publishedDate").split("-")[0]
    description = book_data.get("description")
    number_of_pages = book_data.get("pageCount")

    author_instance, _ = Author.objects.get_or_create(name=author)
    book, _ = Book.objects.get_or_create(
        title=title,
        author=author_instance,
        cover=cover_url,
        year=publication_year,
        description=description,
        number_of_pages=number_of_pages,
    )

    return book


def get_book_details(title: str, author: str) -> dict:
    key = settings.GOOGLE_BOOKS_API_SECRET_KEY
    if not key:
        raise Exception("You must specify GOOGLE_BOOKS_API_SECRET_KEY.")
    GOOGLE_API_KEY = "AIzaSyDhMvIZklh3tpv8Bo9oIzDWnvbLWhToLhg"
    title = title.replace(" ", "+")
    author = author.replace(" ", "+")
    try:
        google_books_url = "https://www.googleapis.com/books/v1/"
        url = (
            f"{google_books_url}volumes?q=inauthor:{author}"
            f"+intitle:{title}&key={GOOGLE_API_KEY}"
        )
        context = ssl._create_unverified_context()
        file = urllib.request.urlopen(url, context=context)
        json_data = file.read()
        file.close()
    except Exception:
        raise Exception("Some errors occurred try later.")

    data = json.loads(json_data)
    if data["totalItems"] == 0:
        raise Exception("No book with this title and author.")
    book_data = data["items"][0]["volumeInfo"]
    return book_data
