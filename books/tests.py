from django.test import TestCase
from django.urls import reverse

from books.models import Book, Author, BookAuthor
from users.models import CustomUser


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="book1", description="description1", isbn="123121")
        book2 = Book.objects.create(title="book2", description="description2", isbn="123122")
        book3 = Book.objects.create(title="book3", description="description3", isbn="123123")

        responce = self.client.get(reverse("books:list") + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(responce, book.title)
        self.assertNotContains(responce, book3.title)

        responce = self.client.get(reverse("books:list") + "?page=2?page_size=2")

        self.assertContains(responce, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="book1", description="description1", isbn="123121")

        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    # def test_book_author(self):
    #     book = Book.objects.create(title="book1", description="description1", isbn="123121")
    #     author = Author.objects.create(first_name="bek", last_name="bekov", email="bek@gmail.com", bio="bek bekov kitobi")
    #     book_author = BookAuthor.objects.create(book=book, author=author)
    #
    #     response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))
    #
    #     self.assertContains(response, book.title, book.description, book.isbn)
    #     self.assertContains(response, author.first_name, author.last_name, author.email, author.bio)
    #     self.assertContains(response, book_author.book, book_author.author)



    def test_search_books(self):
        book1 = Book.objects.create(title="Sport", description="description1", isbn="123121")
        book2 = Book.objects.create(title="Task", description="description2", isbn="123122")
        book3 = Book.objects.create(title="Dog", description="description3", isbn="123123")

        response = self.client.get(reverse("books:list") + "?q=sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=task")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=dog")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)

class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="book1", description="description1", isbn="123121")

        user = CustomUser.objects.create(
            username="bek", first_name="bek", last_name="bekov", email="bek@gmail.com"
        )
        user.set_password("7777")
        user.save()
        self.client.login(username="bek", password="7777")

        self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
            "stars_given": 3,
            "comment": "Nice Book"
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice Book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)

    def test_error_star(self):
        book = Book.objects.create(title="graf", description="description", isbn="971151796718")

        user = CustomUser.objects.create(
            username="bek", first_name="bek", last_name="bekov", email="bek@gmail.com"
        )
        user.set_password("7777")
        user.save()
        self.client.login(username="bek", password="7777")

        response = self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
            "stars_given": 6,
            "comment": "Comment Book"
        })

        self.assertFormError(response, "form", "stars_given", "Ensure this value is less than or equal to 5.")




















