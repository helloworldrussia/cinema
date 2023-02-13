from django.test import TestCase

from movies.filters import MovieFilterSet
from movies.models import Actor, Director, Genre, Movie


class MovieFilterSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.actor_1 = Actor.objects.create(name='Ryan Reynolds')
        cls.actor_3 = Actor.objects.create(name='Tom Cruise')
        cls.actor_2 = Actor.objects.create(name='Arkady Ivanov')

        cls.director_1 = Director.objects.create(name='Steven Spielberg')
        cls.director_2 = Director.objects.create(name='Paul Thomas Anderson')
        cls.director_3 = Director.objects.create(name='Jane Campion')

        cls.genre_1 = Genre.objects.create(name='Comedy')
        cls.genre_2 = Genre.objects.create(name='Drama')
        cls.genre_3 = Genre.objects.create(name='Thriller')

        cls.movie_1 = Movie.objects.create(
            description='Увлекательная комендия о человеке и камне',
            title='Скала',
            director=cls.director_1,
            genre=cls.genre_1
        )
        cls.movie_1.actors.add(cls.actor_1.pk)

        cls.movie_2 = Movie.objects.create(
            description='Всеми любимый фильм в новом жанре',
            title='Скала 2',
            director=cls.director_2,
            genre=cls.genre_2
        )
        cls.movie_2.actors.add(cls.actor_2)

        cls.movie_3 = Movie.objects.create(
            description='Охота. Скала. Добыча.',
            title='Охотник',
            director=cls.director_3,
            genre=cls.genre_3
        )
        cls.movie_3.actors.add(cls.actor_1, cls.actor_3.pk)

        cls.movie_4 = Movie.objects.create(
            description='Тестовое описание',
            title='Фильм Аутсайдер'
        )

    def test_search_filter(self):
        search_query = 'Скала'
        queryset = [self.movie_1, self.movie_2, self.movie_3]
        filtered = MovieFilterSet({'search': search_query})

        self.assertEqual(list(filtered.qs), queryset)

        search_query = self.actor_1.name
        queryset = [self.movie_1, self.movie_3]
        filtered = MovieFilterSet({'search': search_query})

        self.assertEqual(list(filtered.qs), queryset)

        search_query = self.director_1.name
        filtered = MovieFilterSet({'search': search_query})
        queryset = [self.movie_1]

        self.assertEqual(list(filtered.qs), queryset)

    def test_genres_filter(self):
        genres_query = [self.genre_1.pk, self.genre_3.pk]

        filtered = MovieFilterSet(
            {'genres': genres_query}
        )

        expected_data = [self.movie_1, self.movie_3]
        self.assertEqual(list(filtered.qs), expected_data)

        genres_query = [self.genre_1.pk]

        filtered = MovieFilterSet(
            {'genres': genres_query}
        )

        expected_data = [self.movie_1]
        self.assertEqual(list(filtered.qs), expected_data)

    def test_comprehensive_filter(self):
        filters = {
            'genres': [self.genre_3.pk, self.genre_2.pk],
            'search': self.director_2.name
        }

        filtered = MovieFilterSet(filters)
        expected_data = [self.movie_2]

        self.assertEqual(list(filtered.qs), expected_data)

        filters = {
            'genres': [self.genre_1, self.genre_2.pk, self.genre_3],
            'search': self.actor_1.name
        }

        expected_data = [self.movie_1, self.movie_3]
        filtered = MovieFilterSet(filters)

        self.assertEqual(list(filtered.qs), expected_data)

        filters = {
            'genres': [self.genre_1.pk],
            'search': '2'
        }

        filtered = MovieFilterSet(filters)
        expected_data = []

        self.assertEqual(list(filtered.qs), expected_data)
