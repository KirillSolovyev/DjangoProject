from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ..models import Board, Topic, Post, Topic
from ..views import reply_topic


class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Django", description="Test Description")
        self.username = "user1"
        self.password = "123"
        user = User.objects.create_user(name=self.username, password=self.password, email="example@mail.com")
        self.topic = Topic.objects.create(subject="Test subject", board=self.board, starter=user)
        Post.objects.create(message="Hello, Test Test", topic=self.topic, created_by=user)
        self.url = reverse("reply_topic", kwargs={"pk": self.board.pk, "topic_pk": self.topic.pk})
