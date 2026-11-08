"""The Django admin: a full back-office UI for your models, for free.
Create a login with:  python manage.py createsuperuser   then open /admin/"""
from django.contrib import admin

from .models import Author, Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "price", "in_stock"]   # table columns
    list_filter = ["in_stock", "author"]                      # sidebar filters
    search_fields = ["title", "author__name"]                 # search box (follows the FK)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "country"]
