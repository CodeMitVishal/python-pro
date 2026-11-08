"""Solution · Exercise 25: catalog/api.py"""
from django.db.models import Avg, Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author, Book, Review
from .serializers import AuthorSerializer, BookSerializer, ReviewSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = Book.objects.select_related("author").annotate(avg_rating=Avg("reviews__rating"))
        if self.request.query_params.get("in_stock") == "true":
            qs = qs.filter(in_stock=True)
        return qs

    @action(detail=False)
    def cheapest(self, request):
        book = self.get_queryset().order_by("price").first()
        return Response(BookSerializer(book).data if book else None)


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.annotate(book_count=Count("books")).order_by("name")


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        qs = Review.objects.all()
        book = self.request.query_params.get("book")
        return qs.filter(book_id=book) if book else qs
