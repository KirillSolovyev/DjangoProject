from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.urls import resolve, reverse
from django.test import TestCase


class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse("password_change")
        login_url = reverse("login")
        response = self.client.get(url)
        self.assertRedirects(response, f"{login_url}?next={url}")


class PasswordChangeTestCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(username="kirill", email="kirill@mail.com", password="old_password")
        self.url = reverse("password_change")
        self.client.login(username="kirill", password="old_password")
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTest(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })

    def test_redirection(self):
        self.assertRedirects(self.response, reverse("password_change_done"))

    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new_password"))

    def test_user_authentication(self):
        response = self.client.get(reverse("home"))
        user = response.context.get("user")
        self.assertTrue(user.is_authenticated)