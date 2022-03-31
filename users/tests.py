from dataclasses import dataclass

from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "ulugbek",
                "first_name": "Ulugbek",
                "last_name": "Oroqboyev",
                "email": "ulugbek@gmail.com",
                "password": "roigew"}
        )

        user = CustomUser.objects.get(username="ulugbek")

        self.assertEqual(user.first_name, "Ulugbek")
        self.assertEqual(user.last_name, "Oroqboyev")
        self.assertEqual(user.email, "ulugbek@gmail.com")
        self.assertNotEqual(user.password, "roigew")
        self.assertTrue(user.password, "roigew")

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Ulugbek",
                "email": "ulugbek@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "ulugbek",
                "first_name": "Ulugbek",
                "last_name": "Oroqboyev",
                "email": "invalid-email",
                "password": "roigew"}
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username="ulugbek", first_name="oroqboyev")
        user.set_password("parol")
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "ulugbek",
                "first_name": "Ulugbek",
                "last_name": "Oroqboyev",
                "email": "ulugbek@gmail.com",
                "password": "roigew"}
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")

class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="ulugbek", first_name="oroqboyev")
        self.db_user.set_password("somepass")
        self.db_user.save()

    def test_succesful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "ulugbek",
                "password": "somepass"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong_user",
                "password": "somepass"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "ulugbek",
                "password": "312564"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="ulugbek", password="somepass1")

        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)



class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="bek",
            first_name="bekov",
            last_name="bekovich",
            email="bek@gmail.com"
        )
        user.set_password("bek")
        user.save()

        self.client.login(username="bek", password="bek")

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="bek", first_name="bek", last_name="bekov", email="bek@gmail.com"
        )
        user.set_password("7777")
        user.save()
        self.client.login(username="bek", password="7777")

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "bek",
                "first_name": "bek",
                "last_name": "bekovv",
                "email": "bek2@gmail.com",
            }
        )
        user.refresh_from_db()

        self.assertEqual(user.last_name, "bekovv")
        self.assertEqual(user.email, "bek2@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))








































