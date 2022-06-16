from django.contrib import admin

from books import models

to_register = [
    models.Book,
]

admin.site.register(to_register)
