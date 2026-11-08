"""DRF serializers: like pydantic models for Django. They turn model instances into
JSON and validate incoming JSON before it touches the database."""
from rest_framework import serializers

from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(read_only=True)        # comes from .annotate() in the view

    class Meta:
        model = Author
        fields = ["id", "name", "country", "book_count"]


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "author_name", "price", "published", "in_stock"]

    def validate_price(self, value):                             # validate_<field>
        if value <= 0:
            raise serializers.ValidationError("price must be positive")
        return value
