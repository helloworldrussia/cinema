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
            title='Скала'
        )
        cls.movie_1.directors.set([cls.director_1.pk, cls.director_3.pk])
        cls.movie_1.actors.add(cls.actor_2.pk)
        cls.movie_1.genres.add(cls.genre_1.pk)

        cls.movie_2 = Movie.objects.create(
            description='Всеми любимый фильм в новом жанре',
            title='Скала 2'
        )
        cls.movie_2.directors.add(cls.director_2.pk)
        cls.movie_2.actors.set([cls.actor_1.pk, cls.actor_3.pk])
        cls.movie_2.genres.add(cls.genre_2.pk)

        cls.movie_3 = Movie.objects.create(
            description='Охота. Скала. Добыча.',
            title='Охотник'
        )
        cls.movie_3.directors.add(cls.director_3.pk)
        cls.movie_3.actors.add(cls.actor_3.pk)
        cls.movie_3.genres.set([cls.genre_1.pk, cls.genre_3.pk])

    def test_search_filter(self):
        search_query = 'Скала'
        queryset = Movie.objects.all()
        filtered = MovieFilterSet({'search': search_query})

        self.assertEqual(list(filtered.qs), list(queryset))

    def test_actors_filter(self):
        actors_query = [self.actor_1.pk, self.actor_3.pk]

        filtered = MovieFilterSet(
            {'actors': actors_query}
        )

        expected_data = [self.movie_2, self.movie_3]
        self.assertEqual(list(filtered.qs), expected_data)

    def test_directors_filter(self):
        directors_query = [self.director_1.pk, self.director_3.pk]

        filtered = MovieFilterSet(
            {'directors': directors_query}
        )

        expected_data = [self.movie_1, self.movie_3]
        self.assertEqual(list(filtered.qs), expected_data)

    def test_genres_filter(self):
        genres_query = [self.genre_1.pk, self.genre_3.pk]

        filtered = MovieFilterSet(
            {'directors': genres_query}
        )

        expected_data = [self.movie_1, self.movie_3]
        self.assertEqual(list(filtered.qs), expected_data)

    def comprehensive_filter_test(self):
        filters = {
            'actors': [self.actor_3.pk],
            'directors': [self.director_3.pk],
            'genres': [self.genre_1.pk, self.genre_3.pk],
            'search': 'Добыча'
        }

        filtered = MovieFilterSet(filters)

        expected_data = [self.movie_3]

        self.assertEqual(list(filtered.qs), expected_data)
