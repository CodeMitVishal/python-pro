"""Solution · Exercise 25: catalog/models.py with the new Review model."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=2, blank=True)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    published = models.DateField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.title} ({self.author})"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"{self.rating}* for {self.book.title}"
