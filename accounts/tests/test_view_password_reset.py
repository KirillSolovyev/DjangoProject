from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import resolve, reverse
from django.test import TestCase


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse("password_reset")
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve("/reset/")
        self.assertEqual(view.func.view_class, auth_views.PasswordResetView)

    def test_contains_form(self):
        self.assertIsInstance(self.response.context.get("form"), PasswordResetForm)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_form_inputs(self):
        self.assertContains(self.response, "<input", 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = "example@mail.com"
        User.objects.create_user(username="john", email=email, password="123123")
        url = reverse("password_reset")
        self.response = self.client.get(url, {"email": email})

    def test_redirection(self):
        url = reverse("password_reset_done")
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse("password_reset")
        self.response = self.client.get(url, {"email": "dontexist@mail.com"})

    def test_redirection(self):
        url = reverse("password_reset_done")
        self.assertRedirects(self.response, url)

    def test_no_email_sent(self):
        self.assertEqual(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("password_reset_done"))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve("/reset/done/")
        self.assertEqual(view.func.view_class, auth_views.PasswordResetDoneView)
