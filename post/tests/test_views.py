from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from post.models import Channel, Question
from post.forms import post_form


class TestPostViews(TestCase):

	@classmethod
	def setUpTestData(cls):
		user = User.objects.create_user(username="username", password="password")
		user.save()
		Channel.objects.create(name="testing1")
		Channel.objects.create(name="testing2")

	def test_ask(self):
		url = reverse('ask')
		expected_url = "/new/ask"
		self.assertEqual(url, expected_url)
		resp = self.client.get(url)
		# Should redirect to home if not logged in
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp.url, "/")

		# Create an authenticated session
		self.client.login(username="username", password="password")
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, "new.html")
		# Context Variables
		channels = str(Channel.objects.all())
		self.assertEqual(resp.context["metatype"], "question")
		self.assertEqual(str(resp.context["channels"]), channels)
		self.assertIsInstance(resp.context["form"], post_form)

	def test_discuss(self):
		url = reverse('discuss')
		expected_url = "/new/discuss"
		self.assertEqual(url, expected_url)
		resp = self.client.get(url)
		# Should redirect to home if not logged in
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(resp.url, "/")

		# Create an authenticated session
		self.client.login(username="username", password="password")
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, "new.html")
		# Context Variables
		channels = str(Channel.objects.all())
		self.assertEqual(resp.context["metatype"], "discussion")
		self.assertEqual(str(resp.context["channels"]), channels)
		self.assertIsInstance(resp.context["form"], post_form)

	def test_submit_get(self):
		url = reverse('submit', kwargs={"metatype": "question"})
		# Should redirect to home in both cases
		# 1) not logged in
		resp = self.client.get(url)
		self.assertRedirects(resp, "/")
		# 2) logged in
		self.client.login(username="username", password="password")
		resp = self.client.get(url)
		self.assertRedirects(resp, "/")

	def test_submit_post_without_login(self):
		url = reverse('submit', kwargs={"metatype": "question"})
		# Posts without auth must redirect to home
		resp = self.client.post(url, {})
		self.assertRedirects(resp, "/")

	def test_submit_simple_posts(self):
		url = reverse('submit', kwargs={"metatype": "question"})
		title = "Testing question posting"
		desc = "Description of our test question."
		simpledata = {
			"title": title,
			"description": desc,
			"selectedchannels": ""
		}

		self.client.login(username="username", password="password")

		q = Question.objects.all()
		self.assertEqual(len(q), 0)

		# Follow = True makes the client grab the redirected url too.
		resp = self.client.post(url, simpledata, follow=True)
		self.assertEqual(resp.status_code, 200)

		# Tests for the newly created question.
		q = Question.objects.all()
		self.assertEqual(len(q), 1)
		self.assertEqual(q[0].title, title)
		self.assertEqual(q[0].description, desc)
		self.assertEqual(q[0].channels.count(), 0)
		self.assertEqual(q[0].metatype, "question")
		self.assertEqual(q[0].author, "username")

		# Test for posting of a discussion
		url = reverse('submit', kwargs={"metatype": "discussion"})
		resp = self.client.post(url, simpledata, follow=True)
		self.assertEqual(resp.status_code, 200)

		q = Question.objects.all()
		self.assertEqual(len(q), 2)
		self.assertEqual(q[1].metatype, "discussion")

	def test_submit_post_with_channels(self):
		url = reverse('submit', kwargs={"metatype": "question"})
		title = "Testing post posting"
		desc = "Description of our test question with channels."
		simpledata = {
			"title": title,
			"description": desc,
			"selectedchannels": "testing1"
		}

		self.client.login(username="username", password="password")

		resp = self.client.post(url, simpledata, follow=True)
		self.assertEqual(resp.status_code, 200)

		q = Question.objects.first()
		c = Channel.objects.get(name="testing1")
		self.assertEqual(len(Question.objects.all()), 1)
		self.assertEqual(q.title, title)
		self.assertEqual(q.channels.count(), 1)
		self.assertEqual(q.channels.all()[0], c)

		# Test for posting of a discussion
		url = reverse('submit', kwargs={"metatype": "discussion"})
		simpledata["selectedchannels"] = "testing1,testing2"
		resp = self.client.post(url, simpledata, follow=True)
		self.assertEqual(resp.status_code, 200)

		q = Question.objects.last()
		c = str(Channel.objects.all())
		self.assertEqual(q.metatype, "discussion")
		self.assertEqual(q.channels.count(), 2)
		self.assertEqual(str(q.channels.all()), c)

	def test_submit_post_with_errors(self):
		url = reverse('submit', kwargs={"metatype": "question"})
		simpledata = {
			"title": "",
			"description": "",
			"selectedchannels": ""
		}

		# We aren't doing any server side error processing in post model.
		# This isn't a serious problem as we are doing frontside error checking.
		# But if for some reason the javascript has been disabled or someone tries to make an empty post,
		# The server will throw a 500

