from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from books import models


def get_books(request: HttpRequest) -> HttpResponse:
    books: list[models.Book] = list(models.Book.objects.all())
    context = {
        "books": books,
    }
    return render(request, "book_list.html", context)
