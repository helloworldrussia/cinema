from django import forms
from django.test import TestCase

from authentication.forms import SignUpForm


class SignUpFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data = {
            'email': 'user@gmail.com',
            'username': 'good_user',
            'password1': '!passWord!',
            'password2': '!passWord!'
        }

    def test_ok(self):
        form = SignUpForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_existing_fields(self):
        form_fields = SignUpForm().fields

        self.assertEqual(type(form_fields['email']), forms.EmailField)
        self.assertEqual(type(form_fields['username']), forms.CharField)
        self.assertEqual(type(form_fields['password1']), forms.CharField)
        self.assertEqual(type(form_fields['password2']), forms.CharField)

    def test_required_fields(self):
        form = SignUpForm(data={})

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('email'))
        self.assertTrue(form.has_error('username'))
        self.assertTrue(form.has_error('password1'))
        self.assertTrue(form.has_error('password2'))

    def test_password_confirm(self):
        self.form_data['password2'] = 'wrong-password2'
        form = SignUpForm(data=self.form_data)

        expected_error_message = {
            'password_mismatch': 'The two password fields didn’t match.'
        }

        self.assertEqual(form.error_messages, expected_error_message)
