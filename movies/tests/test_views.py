from django.db import connection
from django.test import TestCase
from django.urls import reverse
from django.test.utils import CaptureQueriesContext

from authentication.models import User
from movies.models import Movie, Comment


class MovieListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('movies:movie_list')

    def test_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movie_list.html')

    def test_db_queries_count(self):
        with CaptureQueriesContext(connection) as queries:
            self.client.get(self.url)
            self.assertEqual(2, len(queries))


class MovieDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(
            email='mail@mail.ru',
            username='test_user',
            password='PassWord!'
        )

        cls.user_2 = User.objects.create_user(
            email='gmail@gmail.ru',
            username='test_user_2',
            password='PassWord!'
        )

        cls.movie = Movie.objects.create(
            title='Скала', description='Фильм о героическом подвиге'
        )

        Comment.objects.create(
            author=cls.user_1, movie=cls.movie, text='Хороший фильм', rate=5
        )

        cls.url = reverse('movies:movie_detail', args=(cls.movie.pk,))

    def test_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movie_detail.html')

    def test_create_comment(self):
        data = {
            'rate': 5,
            'user_pk': self.user_2.pk,
            'movie_pk': self.movie.pk,
            'text': 'Good!'
        }
        response = self.client.post(self.url, data=data)
        comment = Comment.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(comment.author, self.user_2)
        self.assertEqual(comment.text, data['text'])
        self.assertEqual(comment.rate, data['rate'])
        self.assertEqual(comment.movie, self.movie)

    def test_re_commenting(self):
        user_comments = Comment.objects.filter(
            author=self.user_1, movie=self.movie
        )

        self.assertEqual(len(user_comments), 1)

        data = {
            'rate': 5,
            'user_pk': self.user_1.pk,
            'movie_pk': self.movie.pk,
            'text': 'Good!'
        }
        response = self.client.post(self.url, data=data)
        user_comments = Comment.objects.filter(
            author=self.user_1, movie=self.movie
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(user_comments), 1)

    def test_db_queries_count(self):
        self.client.force_login(self.user_1)
        with CaptureQueriesContext(connection) as queries:
            self.client.get(self.url)
            self.assertEqual(6, len(queries))

        self.client.logout()
        with CaptureQueriesContext(connection) as queries:
            self.client.get(self.url)
            self.assertEqual(4, len(queries))
