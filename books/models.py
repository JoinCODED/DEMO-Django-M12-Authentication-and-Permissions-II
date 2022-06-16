from django.conf import settings
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=30)
    summary = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="books",
    )

    def __str__(self) -> str:
        return self.title
