from books.models import Book


def get(request):
    return {"books/list.html": Book.objects.all()}

