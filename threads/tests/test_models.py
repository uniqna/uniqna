from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import datetime
from decimal import Decimal
from mptt.models import TreeForeignKey

from post.models import Question
from threads.models import Answer
from root.algorithms import parser
from root.algorithms.vote_score import confidence


class TestAnswer(TestCase):

	@classmethod
	def setUpTestData(cls):
		Question.objects.create(
			title="Test creating a question.",
			description="Test description of a test question.",
			author="digi"
		)
		User.objects.create(username="digi", email="digi@digiops.me", password="asdf")
		User.objects.create(username="jerry", email="jerry@digiops.me", password="asdf")
		cls.q = Question.objects.first()

		# an Answer
		Answer.objects.create(
			question=cls.q,
			description="Test description of an answer.",
			answer_author="jerry"
		)
		cls.a = Answer.objects.first()

		# a Reply
		Answer.objects.create(
			question=cls.q,
			parent=cls.a,
			description="Test description of a reply.",
			answer_author="digi"
		)
		cls.r = Answer.objects.last()

	def test_created_answer(self):
		# The answer object
		a = self.a
		self.assertIsInstance(a, Answer)
		self.assertEqual(a.id, 1)
		# PK must be the id field
		self.assertEqual(a.pk, a.id)
		self.assertEqual(a.description, "Test description of an answer.")
		self.assertEqual(a.answer_author, "jerry")
		self.assertEqual(a.metatype, "question")
		self.assertEqual(a.ups.count(), 0)
		self.assertEqual(a.downs.count(), 0)
		self.assertEqual(a.score, 0)
		self.assertEqual(a.points, 1)
		self.assertEqual(a.edited, False)
		self.assertEqual(a.edited_time.second, a.created_time.second)
		self.assertIsNone(a.parent)

	def test_created_reply(self):
		r = self.r
		self.assertIsInstance(r, Answer)
		self.assertEqual(r.id, 2)
		self.assertEqual(r.description, "Test description of a reply.")
		self.assertEqual(r.answer_author, "digi")
		self.assertEqual(r.parent, self.a)

	def test_field_types(self):
		a = self.a
		r = self.r
		self.assertIsInstance(a.id, int)
		self.assertIsInstance(a.description, str)
		self.assertIsInstance(a.answer_author, str)
		self.assertIsInstance(a.metatype, str)
		self.assertIsInstance(a.points, int)
		self.assertIsInstance(a.edited, bool)
		self.assertIsInstance(a.score, Decimal)
		self.assertIsInstance(a.created_time, datetime)
		self.assertIsInstance(a.edited_time, datetime)
		self.assertIsInstance(r.parent, Answer)

	def test_str(self):
		self.assertEqual(str(self.a), self.a.description)
		self.assertEqual(str(self.r), self.r.description)

	def test_absolute_url(self):
		a = self.a
		r = self.r
		ans_url = "/thread/{}#a{}".format(a.question.id, a.id)
		reply_url = "/thread/{}/reply/{}/".format(r.question.id, r.id)
		self.assertEqual(a.get_absolute_url(), ans_url)
		self.assertEqual(r.get_absolute_url(), reply_url)

	def test_answer_votes(self):
		a = self.a
		digi = User.objects.first()
		jerry = User.objects.last()
		ups = a.ups.count()
		downs = a.downs.count()
		self.assertEqual(a.ups.count(), 0)
		self.assertEqual(a.downs.count(), 0)
		a.ups.add(digi)
		self.assertEqual(a.ups.count(), 1)
		self.assertEqual(a.downs.count(), 0)
		a.downs.add(jerry)
		self.assertEqual(a.ups.count(), 1)
		self.assertEqual(a.downs.count(), 1)
		a.downs.remove(jerry)
		a.ups.add(jerry)
		self.assertEqual(a.ups.count(), 2)
		self.assertEqual(a.downs.count(), 0)
		a.ups.remove(digi)
		self.assertEqual(a.ups.count(), 1)
		a.ups.remove(jerry)
		self.assertEqual(a.ups.count(), 0)
		self.assertEqual(a.downs.count(), 0)

	def test_confidence(self):
		Answer.objects.score_update()
		a = self.a
		self.assertEqual(float(a.score), 0)

		a.ups.add(User.objects.first())
		Answer.objects.score_update()
		a = Answer.objects.first()
		calc_popularity = confidence(1, 0)
		self.assertEqual(a.points, 1)
		self.assertEqual(float(a.score), calc_popularity)

		a.downs.add(User.objects.last())
		Answer.objects.score_update()
		a = Answer.objects.first()
		calc_popularity = confidence(1, 1)
		self.assertEqual(a.points, 0)
		self.assertEqual(float(a.score), calc_popularity)

	def test_get_time(self):
		a = self.a
		t = timezone.localtime(a.created_time)
		tstring = "{}-{}-{} {}:{}".format(
			t.day, t.month,
			t.year, t.hour,
			t.minute
		)
		self.assertEqual(a.get_time(), tstring)

	def test_set_edited_time(self):
		a = Answer.objects.first()
		a.description = "Answer description is now edited."
		a.set_edited_time()
		a.save()
		self.assertTrue(a.edited)
		self.assertNotEqual(a.edited_time, a.created_time)

	def test_get_edited_time(self):
		a = Answer.objects.first()
		t = timezone.localtime(a.edited_time)
		tstring = "{}-{}-{} {}:{}".format(
			t.day, t.month,
			t.year, t.hour,
			t.minute
		)
		self.assertEqual(a.get_edited_time(), tstring)

