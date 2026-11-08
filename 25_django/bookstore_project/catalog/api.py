"""DRF ViewSets: one class = list, create, retrieve, update, delete endpoints.
A router turns them into URLs:  /api/books/  and  /api/books/<id>/"""
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = Book.objects.select_related("author")
        if self.request.query_params.get("in_stock") == "true":     # /api/books/?in_stock=true
            qs = qs.filter(in_stock=True)
        return qs

    @action(detail=False)                                           # extra endpoint: /api/books/cheapest/
    def cheapest(self, request):
        book = self.get_queryset().order_by("price").first()
        return Response(BookSerializer(book).data if book else None)


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):                 # GET only
    serializer_class = AuthorSerializer
    queryset = Author.objects.annotate(book_count=Count("books")).order_by("name")
