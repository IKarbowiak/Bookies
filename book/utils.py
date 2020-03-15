import urllib

import xmltodict
from django.conf import settings

from .models import Author, Book


# there are more info in goodread like rating and author photos
def book_get_or_create(title: str, author: str) -> Book:
    book = Book.objects.filter(title=title, author__name=author).first()
    if book:
        return Book

    book_data = get_book_details(title, author)

    title = book_data["title"]
    author = book_data["authors"]["author"][0]["name"]
    cover_url = book_data.get("image_url")
    publication_year = book_data.get("publication_year")
    description = book_data.get("description")
    number_of_pages = book_data.get("num_pages")

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
    key = settings.GOODREADS_SECRET_KEY
    if not key:
        raise Exception("You must specify GOODREADS_SECRET_KEY.")
    title = title.replace(" ", "+")
    author = author.replace(" ", "+")
    try:
        goodereads_url = "https://www.goodreads.com/book/"
        url = f"{goodereads_url}title.xml?author={author}&key={key}&title={title}"
        file = urllib.request.urlopen(url)
        xml_data = file.read()
        file.close()
    except Exception:
        raise Exception("No book with this title and author.")

    data = xmltodict.parse(xml_data)
    book_data = data["GoodreadsResponse"]["book"]
    return book_data
