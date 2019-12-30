from django.urls import reverse, resolve
from django.test import TestCase

from .. import views
from ..models import Board


class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Django", description="Django Board")
        url = reverse(views.board_topics, kwargs={"pk": self.board.pk})
        self.response = self.client.get(url)

    def test_board_topics_view_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse(views.board_topics, kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve("/boards/1/")
        self.assertEqual(view.func, views.board_topics)

    def test_board_topics_view_contains_navigation_links(self):
        home_url = reverse("home")
        new_topic_url = reverse(views.new_topic, kwargs={"pk": self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(home_url))
        self.assertContains(self.response, 'href="{0}"'.format(new_topic_url))