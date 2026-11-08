from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api, views

app_name = "catalog"

router = DefaultRouter()
router.register("books", api.BookViewSet, basename="book")
router.register("authors", api.AuthorViewSet, basename="author")

urlpatterns = [
    path("", views.BookListView.as_view(), name="book-list"),         # HTML
    path("books/<int:pk>/", views.book_detail, name="book-detail"),   # HTML
    path("api/", include(router.urls)),                               # JSON API
]
