from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth.models import User

from .. import views
from ..models import Board, Topic, Post
from ..forms import NewTopicForm


class HomeTests(TestCase):
	def setUp(self):
		self.board = Board.objects.create(name="Django", description="Board about Django...")
		url = reverse(views.home)
		self.response = self.client.get(url)

	def test_home_view_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_home_url_resolves_home_views(self):
		view = resolve("/")
		self.assertEqual(view.func, views.home)

	def test_home_view_contains_link_to_topics_page(self):
		board_topics_url = reverse(views.board_topics, kwargs={"pk": self.board.pk})
		self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


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
		home_url = reverse(views.home)
		new_topic_url = reverse(views.new_topic, kwargs={"pk": self.board.pk})
		self.assertContains(self.response, 'href="{0}"'.format(home_url))
		self.assertContains(self.response, 'href="{0}"'.format(new_topic_url))


class NewTopicTests(TestCase):
	def setUp(self):
		self.board = Board.objects.create(name="Test board", description="This is test board")
		self.user = User.objects.create(username="Test", email="test@gmail.com", password="123")
		url = reverse(views.new_topic, kwargs={"pk": 1})
		self.response = self.client.get(url)

	def test_contains_form(self):
		form = self.response.context.get("form")
		self.assertIsInstance(form, NewTopicForm)

	def test_new_topic_view_success_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_new_topic_view_not_found_status_code(self):
		url = reverse(views.new_topic, kwargs={"pk": 99})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_new_topic_url_resolves_view(self):
		view = resolve("/boards/1/new/")
		self.assertEqual(view.func, views.new_topic)

	def test_new_topic_view_contains_link_to_board(self):
		board_topic_url = reverse(views.board_topics, kwargs={"pk": self.board.pk})
		self.assertContains(self.response, 'href="{0}"'.format(board_topic_url))

	def test_csrf(self):
		self.assertContains(self.response, "csrfmiddlewaretoken")

	def test_new_topic_valid_post_data(self):
		url = reverse(views.new_topic, kwargs={"pk": 1})
		data = {
			"subject": "Test subject",
			"message": "Test message"
		}
		response = self.client.post(url, data)
		self.assertTrue(Topic.objects.exists())
		self.assertTrue(Post.objects.exists())

	def test_new_topic_invalid_data(self):
		url = reverse(views.new_topic, kwargs={"pk": 1})
		response = self.client.post(url, {})
		self.assertEquals(response.status_code, 200)

	def test_new_topic_empty_data(self):
		url = reverse(views.new_topic, kwargs={"pk": 1})
		response = self.client.post(url, {})
		form = response.context.get("form")
		self.assertEqual(response.status_code, 200)
		self.assertTrue(form.errors)
