from django.contrib.auth.models import User
from django.test import TestCase

from root.algorithms import parser


class TestParser(TestCase):

	@classmethod
	def setUpTestData(cls):
		User.objects.create(username="digi", email="digi@digiops.me", password="asdf")
		User.objects.create(username="jerry", email="jerry@digiops.me", password="asdf")
		cls.u1 = User.objects.get(username='digi')
		cls.u2 = User.objects.get(username='jerry')

	def test_get_user(self):
		self.assertEqual(parser.get_user('digi'), self.u1)
		self.assertEqual(parser.get_user('digi.'), self.u1)
		self.assertEqual(parser.get_user('jerry!'), self.u2)
		self.assertEqual(parser.get_user('idontexist'), False)
		self.assertEqual(parser.get_user('DIGI'), False)
		self.assertEqual(parser.get_user('digi..'), False)

	def test_user_mentions(self):
		parser1 = parser.parse_user_mentions('hi @digi')
		expected1 = "hi <a href='/@digi/'>@digi</a>"
		self.assertEqual(parser1, expected1)
		parser2 = parser.parse_user_mentions('hi @jerry.')
		expected2 = "hi <a href='/@jerry/'>@jerry.</a>"
		self.assertEqual(parser2, expected2)
		parser3 = parser.parse_user_mentions('hi @anony.')
		expected3 = "hi @anony."
		self.assertEqual(parser3, expected3)
