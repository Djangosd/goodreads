from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title="Sport", description="description1", isbn="123121")

        user = CustomUser.objects.create(
            username="bek", first_name="bek", last_name="bekov", email="bek@gmail.com"
        )

        user.set_password("7777")
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="Very good book")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="book")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Nice book")

        response = self.client.get(reverse("home_page") + "?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)




