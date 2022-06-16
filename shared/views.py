from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

User = get_user_model()


def home(request: HttpRequest) -> HttpResponse:
    users: list[User] = list(User.objects.all())

    context = {
        "users": users,
    }

    return render(request, "home.html", context)
