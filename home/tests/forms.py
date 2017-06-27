from django.contrib.auth.models import User
from django.test import TestCase

from home.forms import registration, changePasswordForm


class TestRegisterForm(TestCase):

	@classmethod
	def setUpTestData(cls):
		User.objects.create_user(username="digi", password="password")

	def setUp(self):
		self.data = {
			"username": "digiops",
			"email": "digi@digi.com",
			"password": "password",
			"confirm_password": "password",
			"bio": "diggity diggity dah.",
			"university": "Vellore Institute of Technology, Chennai",
			"course": "B.Tech",
			"school": "SCSE",
			"grad_year": "2020",
		}

	def test_init(self):
		form = registration(self.data)
		self.assertIsInstance(form, registration)
		self.assertTrue(form.is_valid())

	def test_required_fields(self):
		form = registration({})

		self.assertFalse(form.is_valid())
		self.assertTrue("username" in form.errors)
		self.assertTrue("email" in form.errors)
		self.assertTrue("university" in form.errors)
		self.assertTrue("school" in form.errors)
		self.assertTrue("bio" in form.errors)
		self.assertTrue("course" in form.errors)
		self.assertTrue("password" in form.errors)
		self.assertTrue("confirm_password" in form.errors)

	def test_username_errors(self):
		newdata = self.data.copy()
		min_error = ["Ensure this value has at least 4 characters (it has 3)."]
		symbol_error = ['Username not valid.\nOnly use alphabets, numbers and underscore.']
		already_use_error = ['Username "digi" is already in use.']

		# Length errors
		newdata["username"] = "dav"
		form = registration(newdata)
		self.assertFalse(form.is_valid())
		self.assertTrue(form.errors["username"])
		self.assertEqual(form.errors["username"], min_error)

		# Symbol error
		newdata["username"] = "hai$"
		form = registration(newdata)
		self.assertFalse(form.is_valid())
		self.assertTrue(form.errors["username"])
		self.assertEqual(form.errors["username"], symbol_error)

		newdata["username"] = "digi"
		form = registration(newdata)
		self.assertFalse(form.is_valid())
		self.assertTrue(form.errors["username"])
		self.assertEqual(form.errors["username"], already_use_error)

	def test_password_errors(self):
		newdata = self.data.copy()
		pass_error = ["Your passwords do not match."]

		newdata["confirm_password"] = "something else"
		form = registration(newdata)
		self.assertFalse(form.is_valid())
		self.assertTrue(form.errors["confirm_password"])
		self.assertEqual(form.errors["confirm_password"], pass_error)


class TestChangePasswordForm(TestCase):

	@classmethod
	def setUpTestData(cls):
		self.data = {
			"current_password": "old",
			"password": "new",
			"confirm_password": "new"
		}

	def test_init(self):
		data = self.data.copy()
		form = changePasswordForm(data)

		self.assertTrue(form.is_valid())

	def test_required_fields(self):
		form = changePasswordForm({})

		self.assertFalse(form.is_valid())
		self.assertTrue("current_password" in form.errors)
		self.assertTrue("password" in form.errors)
		self.assertTrue("confirm_password" in form.errors)

	def test_password_errors(self):
		newdata = self.data.copy()
		pass_error = ["Your passwords do not match."]

		newdata["confirm_password"] = "something else"
		form = registration(newdata)
		self.assertFalse(form.is_valid())
		self.assertTrue(form.errors["confirm_password"])
		self.assertEqual(form.errors["confirm_password"], pass_error)
