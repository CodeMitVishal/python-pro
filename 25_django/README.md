# Module 25 · Django + Django REST Framework

[← Back to the course](../README.md) · [Slides](../slides/python-pro-slides.pdf)

The batteries-included framework: models and migrations, the admin, views and templates, and a REST API with DRF, in a real project.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Guided tour | [`01_django_tour.py`](01_django_tour.py) | migrate, ORM queries, pages and API through the test client |
| The project | [`bookstore_project/`](bookstore_project/) | settings from env vars, catalog app, admin, templates |
| The API | [`bookstore_project/catalog/api.py`](bookstore_project/catalog/api.py) | serializers, ModelViewSet, router, permissions |
| Tests | [`bookstore_project/catalog/tests.py`](bookstore_project/catalog/tests.py) | `python manage.py test` |

```bash
pip install django djangorestframework
```

```bash
python 25_django/01_django_tour.py
```

## Exercise: Book reviews

Add a Review model, admin, serializer validation, an average rating and a filtered endpoint.

- Start here: [`exercises/ex25_test_reviews.py`](../exercises/ex25_test_reviews.py)
- Solution: [`solutions/ex25_django_reviews/`](../solutions/ex25_django_reviews/)

## Knowledge check

Test yourself with the [Module 25 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 26 · WebSockets, background tasks & caching](../26_realtime_tasks_caching/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
