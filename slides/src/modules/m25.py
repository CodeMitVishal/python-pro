"""Slides · Module 25 · Django + DRF"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 25 · Django + DRF"
DJANGO_SETUP = '''
import django
from django.conf import settings
settings.configure(DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
                   INSTALLED_APPS=["django.contrib.contenttypes"], DEBUG=True)
django.setup()
from django.db import models, connection
from django.test.utils import CaptureQueriesContext
'''

SLIDES = [
 cover("25", "Django + DRF", "The batteries-included framework most Python web jobs ask for: ORM, admin, auth and REST APIs.",
       [("Guided tour", "01_django_tour.py"), ("The bookstore project", "bookstore_project/"),
        ("REST API with DRF", "catalog/api.py"), ("Tests", "catalog/tests.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Django", "Why companies pick Django",
     "A startup needs a shop with users, an admin panel for staff, a database with migrations, forms, and an API for the mobile app. <b>By Friday.</b>",
     "Django ships all of it: <b>ORM, migrations, admin, auth, forms, templates</b>. DRF adds REST APIs. You write the business logic."),

 picture(M, "Request flow", "How Django answers a request (MVT)",
     "&#127970; Django calls it <b>Model-View-Template</b>: the URL router picks a view, the view uses models to talk to the DB, "
     "and a template (or a DRF serializer) turns the result into HTML or JSON. Middleware wraps everything.",
     [("middleware", "security, sessions, auth, CSRF"), ("urls.py", "path(\"books/&lt;int:pk&gt;/\", view)"),
      ("view", "business logic, uses models"), ("model / ORM", "SQL for you"), ("template / serializer", "HTML or JSON")]),

 trace(M, "Project layout", "A Django project at a glance", ["File", "Job"],
       [["<span class=\"m\">manage.py</span>", "runserver, migrate, makemigrations, createsuperuser, test"],
        ["<span class=\"m\">config/settings.py</span>", "INSTALLED_APPS, DATABASES, MIDDLEWARE (read secrets from env!)"],
        ["<span class=\"m\">catalog/models.py</span>", "tables as classes"],
        ["<span class=\"m\">catalog/views.py · urls.py</span>", "pages and their URLs"],
        ["<span class=\"m\">catalog/admin.py</span>", "a full admin UI in a few lines"],
        ["<span class=\"m\">catalog/api.py</span>", "DRF serializers + viewsets"],
        ["<span class=\"m\">catalog/migrations/</span>", "generated schema changes, committed to git"]]),

 code_out(M, "ORM", "QuerySets are lazy and chainable", '''
class Author(models.Model):
    name = models.CharField(max_length=100)
    class Meta: app_label = "shop"

class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    class Meta: app_label = "shop"

with connection.schema_editor() as e:
    e.create_model(Author); e.create_model(Book)
a = Author.objects.create(name="Ramalho")
Book.objects.create(title="Fluent Python", price=49, author=a)
Book.objects.create(title="Python Tricks", price=29, author=a)

qs = Book.objects.filter(price__lt=40).order_by("title")   # no SQL yet
print(qs.query)
print(list(qs.values_list("title", flat=True)))           # runs now''',
     setup=DJANGO_SETUP,
     steps=["<b>filter / exclude / order_by</b> build the query; nothing runs yet.", "It runs when you <b>iterate</b>, slice or call list().",
            "<b>price__lt</b>: field lookups with double underscores."]),

 code_out(M, "ORM", "select_related vs prefetch_related", '''
class Author(models.Model):
    name = models.CharField(max_length=100)
    class Meta: app_label = "shop"
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    class Meta: app_label = "shop"
with connection.schema_editor() as e:
    e.create_model(Author); e.create_model(Book)
for i in range(20):
    Book.objects.create(title=f"b{i}", author=Author.objects.create(name=f"a{i}"))

def count(fn):
    with CaptureQueriesContext(connection) as ctx:
        fn()
    return len(ctx.captured_queries)

print("lazy FK       :", count(lambda: [b.author.name for b in Book.objects.all()]))
print("select_related:", count(lambda: [b.author.name for b in Book.objects.select_related("author")]))
print("prefetch      :", count(lambda: [list(a.books.all()) for a in Author.objects.prefetch_related("books")]))''',
     setup=DJANGO_SETUP,
     steps=["<b>select_related</b>: FK / one-to-one, one <b>JOIN</b>.", "<b>prefetch_related</b>: reverse FK / many-to-many, a second <b>IN</b> query.",
            "Asked in almost every Django interview."]),

 code_out(M, "DRF", "A REST API in three pieces", '''
from rest_framework import permissions, routers, serializers, viewsets

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "price", "author"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("price must be positive")
        return value

class BookViewSet(viewsets.ModelViewSet):        # list/create/retrieve/update/destroy
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

router = routers.DefaultRouter()
router.register("books", BookViewSet)            # /books/ and /books/{id}/''',
     output="GET    /api/books/      -> 200 list\nPOST   /api/books/      -> 201 (logged in)\nGET    /api/books/1/    -> 200\nPATCH  /api/books/1/    -> 200\nDELETE /api/books/1/    -> 204\nPOST price=0            -> 400 {\"price\": [\"price must be positive\"]}",
     steps=["<b>Serializer</b> = validation + JSON (like Pydantic).", "<b>ViewSet</b> + <b>router</b> = all CRUD endpoints.",
            "The project's tests in <b>catalog/tests.py</b> check these."]),

 mistake(M, "Settings", "Shipping the development settings",
     '''
DEBUG = True
SECRET_KEY = "django-insecure-abc123"
ALLOWED_HOSTS = ["*"]''',
     "DEBUG pages leak code and settings to attackers; a committed SECRET_KEY lets them forge sessions.",
     '''
DEBUG = os.environ.get("DJANGO_DEBUG") == "1"
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")
# python manage.py check --deploy''',
     "Settings from the <b>environment</b>; run <b>manage.py check --deploy</b> before going live."),

 trace(M, "Django features", "More things interviewers ask about", ["Feature", "What it is", "Use it for"],
       [["<b>Middleware</b>", "code around every request/response", "auth, CSRF, CORS, request IDs, timing"],
        ["<b>Signals</b>", "hooks like <span class=\"m\">post_save</span>", "small side effects; prefer explicit service calls"],
        ["<b>Migrations</b>", "<span class=\"m\">makemigrations</span> + <span class=\"m\">migrate</span>", "schema changes in git"],
        ["<b>Admin</b>", "auto CRUD UI from models", "internal staff tools"],
        ["<b>transaction.atomic</b>", "all-or-nothing block", "orders + stock updates"],
        ["<b>F() / Q()</b>", "DB-side math / OR conditions", "<span class=\"m\">F(\"stock\") - 1</span> avoids lost updates"]]),

 job(M, "Django", "Django at work", [
     ("Admin for staff in 5 lines", '''
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "price"]'''),
     ("Atomic stock update", '''
Book.objects.filter(pk=pk, stock__gt=0)
            .update(stock=F("stock") - 1)'''),
     ("Tests", '''
class BookAPITests(APITestCase):
    def test_list(self): ...'''),
     ("Production", '''
gunicorn config.wsgi -w 4
collectstatic · whitenoise · Postgres'''),
 ]),

 interview(M, "select_related vs prefetch_related?",
     ["Both fix the <b>N+1</b> problem when you access related objects in a loop.",
      "<b>select_related</b> follows <b>ForeignKey / OneToOne</b> with a SQL <b>JOIN</b>: one query.",
      "<b>prefetch_related</b> handles <b>reverse FK and ManyToMany</b>: a second query with <b>IN (...)</b>, joined in Python.",
      "Verify with django-debug-toolbar or <b>assertNumQueries</b> in tests."],
     '''
Book.objects.select_related("author")
Author.objects.prefetch_related("books")
self.assertNumQueries(2, lambda: ...)''',
     "\"Are QuerySets lazy?\" (yes: they hit the DB only when evaluated: iteration, list(), len(), slicing with a step, bool())."),

 interview(M, "Explain Django's request/response cycle.",
     ["The WSGI/ASGI server passes the request to Django.",
      "<b>Middleware</b> runs (security, session, auth, CSRF) on the way in.",
      "The <b>URL resolver</b> matches urls.py and calls the <b>view</b>.",
      "The view uses <b>models</b> (ORM) and returns a response via a <b>template</b> or DRF <b>serializer</b>.",
      "Middleware runs again on the way out; the server sends the response."],
     None,
     "\"What are signals and when would you avoid them?\" (decoupled hooks like post_save; avoid them for core logic because they hide side effects; call a service explicitly)."),

 recap(M, "Module 25 in 6 lines",
     ["MVT: urls &#8594; view &#8594; models &#8594; template/serializer; middleware around it.",
      "QuerySets are lazy; field lookups like <b>price__lt</b>.",
      "<b>select_related</b> (JOIN) vs <b>prefetch_related</b> (IN query) against N+1.",
      "DRF: <b>Serializer</b> validates, <b>ViewSet</b> + <b>router</b> = CRUD API.",
      "Settings from env; <b>check --deploy</b>; <b>transaction.atomic</b>, <b>F()</b>.",
      "Admin, migrations, tests with <b>APITestCase</b>."],
     "Run the bookstore tests (<b>python manage.py test</b>), then add a <b>/api/authors/</b> endpoint with a test."),
]
