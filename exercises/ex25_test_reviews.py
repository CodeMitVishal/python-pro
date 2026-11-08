"""Exercise 25 · Add book reviews to the Django bookstore

Work inside 25_django/bookstore_project/catalog:

  1. models.py: a Review model
       book    -> ForeignKey to Book, related_name="reviews", on_delete CASCADE
       rating  -> PositiveSmallIntegerField, 1 to 5 (validators MinValueValidator/MaxValueValidator)
       text    -> TextField(blank=True)
       created -> DateTimeField(auto_now_add=True)
     then:  python manage.py makemigrations && python manage.py migrate
  2. admin.py: register Review (list_display: book, rating, created)
  3. serializers.py: ReviewSerializer (fields id, book, rating, text, created) that
     rejects ratings outside 1-5 with the message "rating must be between 1 and 5"
  4. BookSerializer: add a read-only "avg_rating" (None when there are no reviews).
     Tip: annotate the queryset with Avg("reviews__rating") in BookViewSet.get_queryset
  5. api.py + urls.py: a ReviewViewSet at /api/reviews/ (?book=<id> filters by book)

Then copy this file to catalog/tests_reviews.py and run:
    python manage.py test
All tests must pass. Stuck? See solutions/ex25_django_reviews/
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Author, Book, Review


class ReviewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        a = Author.objects.create(name="Ramalho")
        cls.book = Book.objects.create(title="Fluent Python", author=a, price=Decimal("49.90"))
        cls.other = Book.objects.create(title="Other", author=a, price=Decimal("10"))
        Review.objects.create(book=cls.book, rating=5, text="Superb")
        Review.objects.create(book=cls.book, rating=4)

    def setUp(self):
        self.api = APIClient()
        self.api.force_authenticate(User.objects.create_user("vishal"))

    def test_avg_rating_on_books(self):
        books = {b["title"]: b for b in self.api.get("/api/books/").json()["results"]}
        self.assertEqual(books["Fluent Python"]["avg_rating"], 4.5)
        self.assertIsNone(books["Other"]["avg_rating"])

    def test_create_and_filter_reviews(self):
        r = self.api.post("/api/reviews/", {"book": self.other.id, "rating": 3, "text": "ok"})
        self.assertEqual(r.status_code, 201)
        data = self.api.get(f"/api/reviews/?book={self.book.id}").json()
        self.assertEqual(data["count"], 2)

    def test_rating_must_be_1_to_5(self):
        r = self.api.post("/api/reviews/", {"book": self.book.id, "rating": 9})
        self.assertEqual(r.status_code, 400)
        self.assertIn("between 1 and 5", str(r.json()))

    def test_reviews_deleted_with_book(self):
        self.book.delete()
        self.assertEqual(Review.objects.count(), 0)
