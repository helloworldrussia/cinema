from django.test import TestCase
from django import forms
from authentication.models import User
from movies.forms import MovieCommentForm, MovieFilterSearchForm
from movies.models import Movie, Comment, Genre


class MovieCommentFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='gmail@gmail.ru',
            username='test_user_2',
            password='PassWord!'
        )

        cls.movie = Movie.objects.create(
            title='Скала', description='Фильм о героическом подвиге'
        )

        cls.form_data = {
            'rate': 3,
            'text': 'Text',
            'movie_pk': cls.movie.pk,
            'user_pk': cls.user.pk
        }

    def test_ok(self):
        form = MovieCommentForm(data=self.form_data)
        self.assertTrue(form.is_valid())

        last_comment = Comment.objects.last()

        self.assertEqual(last_comment.author, self.user)
        self.assertEqual(last_comment.movie, self.movie)
        self.assertEqual(last_comment.author, self.user)
        self.assertEqual(last_comment.text, self.form_data['text'])
        self.assertEqual(last_comment.rate, self.form_data['rate'])

    def test_existing_fields(self):
        form_fields = MovieCommentForm().fields

        self.assertEqual(type(form_fields['rate']), forms.ChoiceField)
        self.assertEqual(type(form_fields['text']), forms.CharField)
        self.assertEqual(type(form_fields['movie_pk']), forms.IntegerField)
        self.assertEqual(type(form_fields['user_pk']), forms.IntegerField)

    def test_required_fields(self):
        form = MovieCommentForm(data={})

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('rate'))
        self.assertTrue(form.has_error('text'))
        self.assertTrue(form.has_error('movie_pk'))
        self.assertTrue(form.has_error('user_pk'))

    def test_re_commenting(self):
        form = MovieCommentForm(data=self.form_data)
        self.assertTrue(form.is_valid())

        form = MovieCommentForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        expected_error_message = {
            'movie_and_user_unique': [u'Comment with this author and movie already exists.']
        }

        self.assertEqual(form._errors, expected_error_message)

    def test_rate_validation(self):
        self.form_data['rate'] = 6

        form = MovieCommentForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        expected_error_message = {
            'rate': [u'Select a valid choice. 6 is not one of the available choices.']
        }

        self.assertEqual(form._errors, expected_error_message)

    def test_user_pk_validation(self):
        self.form_data['user_pk'] = 'word'

        form = MovieCommentForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        expected_error_message = {
            'user_pk': [u'Enter a whole number.']
        }

        self.assertEqual(form._errors, expected_error_message)

        self.form_data['user_pk'] = 1001

        form = MovieCommentForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        expected_error_message = {
            'user_pk': [u'Invalid user_pk.']
        }

        self.assertEqual(form._errors, expected_error_message)

    def test_movie_pk_validation(self):
        self.form_data['movie_pk'] = 'word'

        form = MovieCommentForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        expected_error_message = {
            'movie_pk': [u'Enter a whole number.']
        }

        self.assertEqual(form._errors, expected_error_message)

        self.form_data['movie_pk'] = 1001

        form = MovieCommentForm(data=self.form_data)
        self.assertFalse(form.is_valid())

        expected_error_message = {
            'movie_pk': [u'Invalid movie_pk.']
        }

        self.assertEqual(form._errors, expected_error_message)


# class MovieFilterSearchForm(forms.Form):
#     search = forms.CharField(label='Search', required=False)
#     genres = forms.ModelChoiceField(
#         Genre.objects.all(), required=False, empty_label='Genre'
#     )
class MovieFilterSearchFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = Genre.objects.create(
            name='Thriller'
        )

    def test_ok(self):
        form = MovieFilterSearchForm(
            {'search': 'Поисковый запрос', 'genres': self.genre.pk}
        )
        self.assertTrue(form.is_valid())

    def test_existing_fields(self):
        form_fields = MovieFilterSearchForm().fields

        self.assertEqual(type(form_fields['search']), forms.CharField)
        self.assertEqual(type(form_fields['genres']), forms.ModelChoiceField)

    def test_required_fields(self):
        form = MovieFilterSearchForm(data={})

        self.assertTrue(form.is_valid())
