from django.db.models import QuerySet
from django.test import TestCase

from authentication.models import User
from movies.mixins import MovieRecommender
from movies.models import Movie, Genre, Director, Actor, Comment


class MovieRecommenderTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='mail@mail.ru',
            username='test_user',
            password='PassWord!'
        )

        cls.recommender = MovieRecommender()
        cls.recommender.user = cls.user

        cls.actor_1 = Actor.objects.create(name='Ryan Reynolds')
        cls.actor_2 = Actor.objects.create(name='Arkady Ivanov')
        cls.actor_3 = Actor.objects.create(name='Tom Cruise')
        cls.actor_4 = Actor.objects.create(name='Good Actor')
        cls.actor_5 = Actor.objects.create(name='Bad Actor')

        cls.director_1 = Director.objects.create(name='Steven Spielberg')
        cls.director_2 = Director.objects.create(name='Paul Thomas Anderson')
        cls.director_3 = Director.objects.create(name='Jane Campion')
        cls.director_4 = Director.objects.create(name='Svetlana Director')
        cls.director_5 = Director.objects.create(name='Good Director')

        cls.genre_1 = Genre.objects.create(name='Comedy')
        cls.genre_2 = Genre.objects.create(name='Drama')
        cls.genre_3 = Genre.objects.create(name='Thriller')
        cls.genre_4 = Genre.objects.create(name='Musical')
        cls.genre_5 = Genre.objects.create(name='Cartoon')

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
            title='Фильм Аутсайдер',
            director=cls.director_4,
            genre=cls.genre_4
        )
        cls.movie_4.actors.add(cls.actor_4.pk)

        cls.movie_5 = Movie.objects.create(
            description='Описание',
            title='Чебурашка',
            director=cls.director_5,
            genre=cls.genre_5
        )
        cls.movie_5.actors.add(cls.actor_5.pk)

    def test_without_comments(self):
        queryset = self.recommender.get_suggestions()
        expected_value = Movie.objects.all()

        self.assertEqual(list(queryset), list(expected_value))
        self.assertEqual(type(queryset), QuerySet)

    def test_display_priority(self):
        Comment.objects.create(
            author=self.user,
            movie=self.movie_3,
            text='I like it!',
            rate=4
        )
        Comment.objects.create(
            author=self.user,
            movie=self.movie_5,
            text='Good',
            rate=5
        )

        queryset = self.recommender.get_suggestions()
        expected_value = [
            self.movie_1, self.movie_3, self.movie_5,
            self.movie_2, self.movie_4
        ]

        self.assertEqual(list(queryset), expected_value)

    def test_exclusion_of_unloved_parameters(self):
        Comment.objects.create(
            author=self.user,
            movie=self.movie_3,
            text='Terribly',
            rate=1
        )

        Comment.objects.create(
            author=self.user,
            movie=self.movie_2,
            text='Nothing interesting',
            rate=2
        )

        Comment.objects.create(
            author=self.user,
            movie=self.movie_4,
            text='Nothing interesting',
            rate=3
        )

        queryset = self.recommender.get_suggestions()
        expected_value = [
            self.movie_5
        ]

        self.assertEqual(list(queryset), expected_value)

    def test_ok(self):
        Comment.objects.create(
            author=self.user,
            movie=self.movie_5,
            text='Good',
            rate=5
        )

        Comment.objects.create(
            author=self.user,
            movie=self.movie_3,
            text='Terribly',
            rate=1
        )

        queryset = self.recommender.get_suggestions()
        expected_value = [
            self.movie_5, self.movie_2, self.movie_4
        ]

        self.assertEqual(list(queryset), expected_value)