from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board, Post, Topic
from ..views import PostUpdateView


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Django", description="Test board")
        self.username = "test"
        self.password = "123"
        user = User.objects.create_user(username=self.username, email="example@mail.com", password=self.password)
        self.topic = Topic.objects.create(subject="Test subject", board=self.board, starter=user)
        self.post = Post.objects.create(message="Hello, MSG", topic=self.topic, created_by=user)
        self.url = reverse("edit_post", kwargs={
            "pk": self.board.pk,
            "topic_pk": self.topic.pk,
            "post_pk": self.post.pk
        })


class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse("login")
        response = self.client.get(self.url)
        self.assertRedirects(response, "{login_url}?next={url}".format(login_url=login_url, url=self.url))


class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = "user1"
        password = "123"
        user = User.objects.create_user(username=username, password=password, email="ex@mail.com")
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 404)


class PostUpdateViewTests(PostUpdateViewTestCase):
    def test_update_resolves_view(self):
        view = resolve("/boards/{pk}/topics/{topic_pk}/posts/{post_pk}/edit/"
                       .format(pk=self.board.pk, topic_pk=self.topic.pk, post_pk=self.post.pk))
        self.assertEqual(view.func.__name__, PostUpdateView.__name__)
