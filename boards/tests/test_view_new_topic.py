from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth.models import User

from .. import views
from ..models import Board, Topic, Post
from ..forms import NewTopicForm


class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Test board", description="This is test board")
        self.user = User.objects.create_user(username="Test", email="test@gmail.com", password="123")
        self.client.login(username="Test", password="123")
        url = reverse("new_topic", kwargs={"pk": 1})
        self.response = self.client.get(url)

    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_view_success_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse("new_topic", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_view(self):
        view = resolve("/boards/1/new/")
        self.assertEqual(view.func, views.new_topic)

    def test_new_topic_view_contains_link_to_board(self):
        board_topic_url = reverse("board_topics", kwargs={"pk": self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topic_url))

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_new_topic_valid_post_data(self):
        url = reverse("new_topic", kwargs={"pk": 1})
        data = {
            "subject": "Test subject",
            "message": "Test message"
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_data(self):
        url = reverse("new_topic", kwargs={"pk": 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_empty_data(self):
        url = reverse("new_topic", kwargs={"pk": 1})
        response = self.client.post(url, {})
        form = response.context.get("form")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name="Django", description="Django")
        self.url = reverse("new_topic", kwargs={"pk": 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse("login")
        self.assertRedirects(self.response, f"{login_url}?next={self.url}")
