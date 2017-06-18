from django.test import TestCase
from api.models import UsernameSnippet


class TestUsernameSnippet(TestCase):

	@classmethod
	def setUpTestData(cls):
		UsernameSnippet.objects.create(available=True)

	def test_existence(self):
		u = UsernameSnippet.objects.first()
		self.assertIsInstance(u, UsernameSnippet)
		self.assertEqual(u.available, True)

	def test_field_types(self):
		u = UsernameSnippet.objects.first()
		self.assertIsInstance(u.available, bool)
