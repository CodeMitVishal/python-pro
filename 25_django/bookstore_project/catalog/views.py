"""HTML views: a function-based view and a class-based view (Django's "MTV":
Model -> Template -> View, where the view connects the two)."""
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Book


def book_detail(request, pk: int):
    book = get_object_or_404(Book.objects.select_related("author"), pk=pk)   # 404 if missing
    return render(request, "catalog/book_detail.html", {"book": book})


class BookListView(ListView):                     # a generic view: listing + pagination built in
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"
    paginate_by = 20

    def get_queryset(self):
        qs = Book.objects.select_related("author")  # 1 query with a JOIN, no N+1 (Module 23!)
        q = self.request.GET.get("q", "")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(author__name__icontains=q))
        return qs
