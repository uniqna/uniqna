from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.test import TestCase

from markdown2 import markdown

from post.models import Channel, Question
from threads.forms import reply_form
from threads.models import Answer


class TestThreadViewsGet(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.digi = User.objects.create_user(username="digi", password="password")
		cls.digi.save()
		cls.jerry = User.objects.create_user(username="jerry", password="password")
		cls.jerry.save()
		cls.q = Question.objects.create(
			title="Testing thread views.",
			metatype="discussion",
			description="Ello there mate",
			author="digi"
		)
		Channel.objects.create(name="testing1")
		Channel.objects.create(name="testing2")
		slug = slugify(cls.q.title)
		cls.url = reverse('thread', args=[cls.q.id, slug])

	def test_thread_not_logged(self):
		# Thread not logged in test
		url = self.url
		expected_url = self.q.get_absolute_url()
		self.assertEqual(url, expected_url)
		resp = self.client.get(url)
		print(resp)
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, "thread.html")
		self.assertTemplateUsed(resp, "contribute_modal.html")
		self.assertTemplateUsed(resp, "thread_replies.html")
		self.assertTemplateUsed(resp, "reply_modal.html")
		self.assertTemplateUsed(resp, "reply_author_modal.html")
		# The text which is shown when there are no users
		self.assertContains(resp, 'Hey there, stranger? If you want to contribute to this discussion, please log in so that we can recognise you! :D')

	def test_thread_logged(self):
		# Thread logged test with no answers
		url = self.url

		self.client.login(username="digi", password="password")
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, "thread.html")
		# Context Variables
		self.assertEqual(resp.context["post"], self.q)
		self.assertEqual(len(resp.context["nodes"]), 0)
		self.assertIsInstance(resp.context["form"], reply_form)

	def test_thread_delete(self):
		# Test whether the delete button is there
		# just for the author.
		q = self.q
		url = self.url
		delete_url = reverse('delete_post', args=[q.id])

		# Author
		self.client.login(username="digi", password="password")
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context["post"], q)
		self.assertContains(resp, delete_url)
		self.assertTemplateUsed(resp, "thread_author_panel.html")
		self.client.logout()

		# Not the author
		self.client.login(username="jerry", password="password")
		resp = self.client.get(url)
		self.assertEqual(resp.context["post"], q)
		self.assertNotContains(resp, delete_url)

	def test_thread_nodes(self):
		# Test thread with answers
		url = self.url
		a = Answer.objects.create(
			question=self.q,
			description="Hello answer.",
			answer_author="digi"
		)
		nodes = Answer.objects.all()
		for node in nodes:
			node.description = markdown(node.description, extras=["tables", "cuddled-lists"])

		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context["post"], self.q)
		self.assertEqual(str(resp.context["nodes"]), str(nodes))


"""
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

"""


class TestMarkdown(TestCase):

	@classmethod
	def setUpTestData(cls):
		u = User.objects.create_user(username="digi", password="password")
		q = Question.objects.create(
			title="The title of the question.",
			description="# Header\n**bold**\n*italic*",
			author="digi"
		)
		a = Answer.objects.create(
			question=q,
			description="### Small header\n**bold**\n*italic*",
			answer_author="digi"
		)
		slug = slugify(q.title)
		url = reverse('thread', args=[q.id, slug])
		cls.q = q
		cls.url = url

	def test_question_desc(self):
		resp = self.client.get(self.url)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context["post"], self.q)
		desc = markdown(self.q.description, extras=["tables", "cuddled-lists"])
		self.assertEqual(resp.context["description"], desc)

	def test_answer_desc(self):
		resp = self.client.get(self.url)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.context["post"], self.q)
		node = Answer.objects.first()
		node.description = markdown(node.description, extras=["tables", "cuddled-lists"])
		self.assertEqual(resp.context["nodes"][0], node)
