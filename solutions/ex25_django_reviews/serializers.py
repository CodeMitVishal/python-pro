"""Solution · Exercise 25: catalog/serializers.py"""
from rest_framework import serializers

from .models import Author, Book, Review


class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "country", "book_count"]


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    avg_rating = serializers.FloatField(read_only=True)     # from .annotate(avg_rating=Avg(...))

    class Meta:
        model = Book
        fields = ["id", "title", "author", "author_name", "price", "published", "in_stock",
                  "avg_rating"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("price must be positive")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    # Declared explicitly so OUR message is used instead of the model validators' default one
    rating = serializers.IntegerField()

    class Meta:
        model = Review
        fields = ["id", "book", "rating", "text", "created"]

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("rating must be between 1 and 5")
        return value
