from django.db import connection
from django.test import TestCase
from django.urls import reverse
from django.test.utils import CaptureQueriesContext

from authentication.models import User
from movies.models import Actor, Director, Genre, Movie

""" TODO Добавить тесты комментариев и постеров """


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
        cls.user = User.objects.create_user(
            email='mail@mail.ru',
            username='test_user',
            password='PassWord!'
        )
        movie = Movie.objects.create(
            title='Скала', description='Фильм о героическом подвиге'
        )
        cls.url = reverse('movies:movie_detail', args=(movie.pk,))

    def test_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movie_detail.html')

    def test_db_queries_count(self):
        self.client.force_login(self.user)
        with CaptureQueriesContext(connection) as queries:
            self.client.get(self.url)
            self.assertEqual(4, len(queries))
