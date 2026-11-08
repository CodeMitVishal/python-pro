"""Django tests: each test runs in a transaction that's rolled back, on a fresh test DB.
Run:  python manage.py test"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Author, Book


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):                      # created once for the whole class
        martin = Author.objects.create(name="Robert C. Martin", country="US")
        Book.objects.create(title="Clean Code", author=martin, price=Decimal("34.50"))
        Book.objects.create(title="Clean Architecture", author=martin, price=Decimal("29.90"),
                            in_stock=False)

    def test_html_list_and_search(self):
        r = self.client.get(reverse("catalog:book-list"), {"q": "architecture"})
        self.assertContains(r, "Clean Architecture")
        self.assertNotContains(r, "Clean Code<")

    def test_detail_404(self):
        self.assertEqual(self.client.get("/books/999/").status_code, 404)

    def test_api_list_and_filter(self):
        api = APIClient()
        data = api.get("/api/books/").json()
        self.assertEqual(data["count"], 2)
        self.assertEqual(api.get("/api/books/?in_stock=true").json()["count"], 1)
        self.assertEqual(api.get("/api/books/cheapest/").json()["title"], "Clean Architecture")
        self.assertEqual(api.get("/api/authors/").json()["results"][0]["book_count"], 2)

    def test_api_write_needs_login_and_valid_price(self):
        api = APIClient()
        author = Author.objects.get().id
        payload = {"title": "Python Pro", "author": author, "price": "0"}
        self.assertEqual(api.post("/api/books/", payload).status_code, 403)   # read-only for guests
        api.force_authenticate(User.objects.create_user("vishal"))
        r = api.post("/api/books/", payload)
        self.assertEqual(r.status_code, 400)
        self.assertIn("price must be positive", str(r.json()))
        payload["price"] = "19.99"
        self.assertEqual(api.post("/api/books/", payload).status_code, 201)
