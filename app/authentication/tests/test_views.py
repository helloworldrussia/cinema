from django.test import TestCase
from django.urls import reverse

from authentication.models import User


# class UserPageViewTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(
#             email='test@mail.ru',
#             username='test_username',
#             password='test_password'
#         )
#
#     def test_deny_anonymous(self):
#         response = self.client.get('/auth/', follow=True)
#         self.assertRedirects(response, '/auth/sign-in/?next=/auth/')
#
#     def test_ok(self):
#         self.client.force_login(self.user)
#         response = self.client.get('/client/', follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'user_page.html')
#         self.assertContains(response, self.user.email)


class SignUpViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {
            'username': 'test_user',
            'email': 'test@mail.com',
            'password1': 'Parol213!',
            'password2': 'Parol213!',
        }
        cls.user = User.objects.create_user(
            email='test@mail.ru',
            username='test_username',
            password='test_password'
        )
        cls.url = reverse('authentication:sign_up')

    def test_ok(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'sign_up.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, reverse('authentication:sign_in'))

        user = User.objects.last()
        self.assertEqual(user.email, self.data['email'])
        self.assertEqual(user.username, self.data['username'])

    def test_required_fields(self):
        response = self.client.post(self.url)

        self.assertFormError(response, 'form', 'email', 'This field is required.')
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password1', 'This field is required.')
        self.assertFormError(response, 'form', 'password2', 'This field is required.')

    def test_duplicate_account(self):
        data = {
            'email': 'test@mail.ru',
            'username': 'test_username',
            'password': 'Password444!!!!'
        }

        response = self.client.post(self.url, data)

        self.assertFormError(response, 'form', 'email', 'User with this Email already exists.')
        self.assertFormError(response, 'form', 'username', 'User with this Username already exists.')
        self.client.post(self.url, self.data)

        response = self.client.post(self.url, self.data)

        self.assertFormError(response, 'form', 'email', 'User with this Email already exists.')
        self.assertFormError(response, 'form', 'username', 'User with this Username already exists.')


class SignInViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@mail.ru',
            username='test_username',
            password='test_password'
        )
        cls.url = reverse('authentication:sign_in')
        cls.movie_list_url = reverse('movies:movie_list')

    def test_ok(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_in.html')

        data = {
            'username': 'test@mail.ru',
            'password': 'test_password'
        }

        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.movie_list_url)

        response = self.client.get(self.movie_list_url)
        self.assertEqual(response.context['user'].email, data['username'])

    def test_required_fields(self):
        response = self.client.post(self.url, {})

        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_wrong_auth_data(self):
        wrong_data_1 = {
            'username': 'wrong@mail.ru',
            'password': 'test_password'
        }
        wrong_data_2 = {
            'username': 'test@mail.ru',
            'password': 'wrong'
        }
        data = {
            'username': 'test@mail.ru',
            'password': 'test_password'
        }
        response = self.client.post(self.url, wrong_data_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('AnonymousUser', response.context['user'].__str__())

        response = self.client.post(self.url, wrong_data_2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('AnonymousUser', response.context['user'].__str__())

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)


class LogoutViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@mail.ru',
            username='test_username',
            password='test_password'
        )
        cls.logout_url = reverse('authentication:logout')
        cls.sign_in_url = reverse('authentication:sign_in')
        cls.movie_list_url = reverse('movies:movie_list')

    def test_ok(self):
        self.client.force_login(self.user)

        response = self.client.get(self.movie_list_url)
        self.assertEqual(response.context['user'].email, 'test@mail.ru')

        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.sign_in_url)

        response = self.client.get(self.sign_in_url)
        self.assertEqual(response.context['user'].__str__(), 'AnonymousUser')


class PasswordChangeViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@mail.ru',
            username='test_username',
            password='test_password'
        )
        cls.data = {
            'username': 'test@mail.ru',
            'password': 'test_password'
        }
        cls.password_change_url = reverse('authentication:password_change')
        cls.sign_in_url = reverse('authentication:sign_in')
        cls.movie_list_url = reverse('movies:movie_list')

    def test_ok(self):
        self.client.force_login(self.user)

        data = {
            'old_password': 'test_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        }
        response = self.client.post(self.password_change_url, data)
        self.assertRedirects(response, self.movie_list_url)

        self.client.logout()

        data = {
            'username': self.data['username'],
            'password': data['new_password1']
        }
        self.client.post(self.sign_in_url, data)
        self.assertRedirects(response, self.movie_list_url)

    def test_deny_anonymous(self):
        response = self.client.get(self.password_change_url)
        self.assertRedirects(
            response, self.sign_in_url + '?next=' + self.password_change_url
        )

    def test_required_fields(self):
        self.client.force_login(self.user)
        response = self.client.post(self.password_change_url, {})

        self.assertFormError(response, 'form', 'old_password', 'This field is required.')
        self.assertFormError(response, 'form', 'new_password1', 'This field is required.')
        self.assertFormError(response, 'form', 'new_password2', 'This field is required.')

    def test_wrong_old_password(self):
        self.client.force_login(self.user)

        data = {
            'old_password': 'wrong_old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        }
        response = self.client.post(self.password_change_url, data)
        self.assertFormError(response,
                             'form',
                             'old_password',
                             'Your old password was entered incorrectly. Please enter it again.'
                             )
