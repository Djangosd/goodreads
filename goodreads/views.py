from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View

from books.models import BookReview, Book

from django.shortcuts import render_to_response
from django.template import RequestContext


class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 4)
        paginator = Paginator(books, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        return render(
            request,
            "books/list.html",
            {"page_obj": page_obj, "search_query": search_query}
        )

def landing_page(request):
    return render(request, "landing.html")


def home_page(request):
    book_reviews = BookReview.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 10)
    paginator = Paginator(book_reviews, page_size)

    page_num = request.GET.get('page', 1)
    page_object = paginator.get_page(page_num)


    return render(request, "home.html", {"page_obj": page_object})


# Shopping Page
def shopping_page(request):
    return render(request, "shopping.html")

def community_page(request):
    return render(request, "community.html")

def notice_page(request):
    return render(request, "notice.html")

def telephone_page(request):
    return render(request, "telephone.html")











