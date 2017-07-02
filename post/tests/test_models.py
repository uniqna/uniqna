from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify

from decimal import Decimal

from post.models import Question, Channel
from root.algorithms.popularity import _popularity


class TestChannel(TestCase):

	@classmethod
	def setUpTestData(cls):
		Channel.objects.create(name="testing", detail="testing channel")
		Channel.objects.create(name="colored", detail="colored channel", color="#afafaf")

	def test_created_channel(self):
		c = Channel.objects.first()
		self.assertIsInstance(c, Channel)
		self.assertEqual(c.name, "testing")
		self.assertEqual(c.detail, "testing channel")
		self.assertEqual(c.color, "#673AB7")

		cc = Channel.objects.last()
		self.assertIsInstance(cc, Channel)
		self.assertEqual(cc.name, "colored")
		self.assertEqual(cc.detail, "colored channel")
		self.assertEqual(cc.color, "#afafaf")

	def test_field_types(self):
		c = Channel.objects.first()
		self.assertIsInstance(c.name, str)
		self.assertIsInstance(c.detail, str)
		self.assertIsInstance(c.color, str)

	def test_str(self):
		c = Channel.objects.first()
		cstr = c.name + " - " + c.detail
		self.assertEqual(str(c), cstr)


class TestQuestion(TestCase):

	@classmethod
	def setUpTestData(cls):
		Question.objects.create(
			title="Test creating a question.",
			description="Test description of a test question.",
			author="digi"
		)
		Channel.objects.create(name="testing")
		User.objects.create(username="digi", email="digi@digiops.me", password="asdf")
		User.objects.create(username="jerry", email="jerry@jerry.me", password="jkl;")

	def test_created_question(self):
		q = Question.objects.first()
		self.assertIsInstance(q, Question)
		self.assertEqual(q.id, 1)
		# PK must be the id field
		self.assertEqual(q.pk, q.id)
		self.assertEqual(q.title, "Test creating a question.")
		self.assertEqual(q.description, "Test description of a test question.")
		self.assertEqual(q.author, "digi")
		self.assertEqual(q.metatype, "question")
		self.assertEqual(q.answers, 0)
		self.assertEqual(q.ups.count(), 0)
		self.assertEqual(q.downs.count(), 0)
		self.assertEqual(float(q.hot), 1000.1230000)
		self.assertEqual(q.points, 1)
		self.assertEqual(q.channels.count(), 0)
		self.assertIsNone(q.flair_icon)
		self.assertIsNone(q.flair)

	def test_field_types(self):
		q = Question.objects.first()
		self.assertIsInstance(q.title, str)
		self.assertIsInstance(q.description, str)
		self.assertIsInstance(q.author, str)
		self.assertIsInstance(q.metatype, str)
		self.assertIsInstance(q.answers, int)
		self.assertIsInstance(q.ups.count(), int)
		self.assertIsInstance(q.downs.count(), int)
		self.assertIsInstance(q.channels.count(), int)
		self.assertIsInstance(q.points, int)
		self.assertIsInstance(q.hot, Decimal)

	def test_str(self):
		q = Question.objects.first()
		self.assertEqual(str(q), q.title)

	def test_absolute_url(self):
		q = Question.objects.first()
		url = "/thread/{}-{}".format(q.id, slugify(q.title))
		self.assertEqual(q.get_absolute_url(), url)

	def test_question_channel(self):
		q = Question.objects.first()
		c = Channel.objects.first()
		self.assertEqual(q.channels.count(), 0)
		q.channels.add(c)
		self.assertEqual(q.channels.count(), 1)
		qc = q.channels.all()[0]
		self.assertEqual(qc, c)
		q.channels.remove(c)
		self.assertEqual(q.channels.count(), 0)

	def test_question_votes(self):
		q = Question.objects.first()
		digi = User.objects.first()
		jerry = User.objects.last()
		ups = q.ups.count()
		downs = q.downs.count()
		self.assertEqual(q.ups.count(), 0)
		self.assertEqual(q.downs.count(), 0)
		q.ups.add(digi)
		self.assertEqual(q.ups.count(), 1)
		self.assertEqual(q.downs.count(), 0)
		q.downs.add(jerry)
		self.assertEqual(q.ups.count(), 1)
		self.assertEqual(q.downs.count(), 1)
		q.downs.remove(jerry)
		q.ups.add(jerry)
		self.assertEqual(q.ups.count(), 2)
		self.assertEqual(q.downs.count(), 0)
		q.ups.remove(digi)
		self.assertEqual(q.ups.count(), 1)
		q.ups.remove(jerry)
		self.assertEqual(q.ups.count(), 0)
		self.assertEqual(q.downs.count(), 0)

	def test_popularity(self):
		Question.objects.popularity_update()
		q = Question.objects.first()
		calc_popularity = _popularity(0, 0, q.created_time)
		self.assertEqual(float(q.hot), calc_popularity)

		q.ups.add(User.objects.first())
		Question.objects.popularity_update()
		calc_popularity = _popularity(1, 0, q.created_time)
		self.assertEqual(float(q.hot), calc_popularity)

		q.downs.add(User.objects.last())
		Question.objects.popularity_update()
		calc_popularity = _popularity(1, 1, q.created_time)
		self.assertEqual(float(q.hot), calc_popularity)

	def test_get_time(self):
		q = Question.objects.first()
		t = timezone.localtime(q.created_time)
		tstring = "{}-{}-{} {}:{}".format(
			t.day, t.month,
			t.year, t.hour,
			t.minute
		)
		self.assertEqual(q.get_time(), tstring)
