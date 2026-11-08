"""Models: each class is a table. Django creates the migrations for you:
    python manage.py makemigrations     (write migration files from model changes)
    python manage.py migrate            (apply them to the database)
"""
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=2, blank=True)     # blank=True: optional in forms

    def __str__(self) -> str:                                 # shown in the admin
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    price = models.DecimalField(max_digits=7, decimal_places=2)   # money: never use float
    published = models.DateField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]                                  # default sort order

    def __str__(self) -> str:
        return f"{self.title} ({self.author})"
