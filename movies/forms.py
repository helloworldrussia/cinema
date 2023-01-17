from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from authentication.models import User
from django.forms.widgets import HiddenInput

from movies.models import Genre, Comment, Movie


class MovieFilterSearchForm(forms.Form):
    search = forms.CharField(label='Search', required=False)
    genres = forms.ModelChoiceField(
        Genre.objects.all(), required=False, empty_label='Genre'
    )


class MovieCommentForm(forms.Form):
    RATING_CHOICES = (
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐')
    )
    rate = forms.ChoiceField(choices=RATING_CHOICES)
    text = forms.CharField(widget=forms.Textarea)
    movie_pk = forms.IntegerField(widget=HiddenInput)
    user_pk = forms.IntegerField(widget=HiddenInput)

    def is_valid(self):
        if super().is_valid():
            if self.create_comment():
                return True

        return False

    def create_comment(self):
        movie = Movie.objects.get(pk=self.cleaned_data.get('movie_pk'))
        user = User.objects.get(pk=self.cleaned_data.get('user_pk'))

        try:
            Comment.objects.create(
                author=user,
                movie=movie,
                text=self.cleaned_data.get('text'),
                rate=self.cleaned_data.get('rate')
            )
        except ValidationError:
            self._errors['movie_and_user_unique'] = ErrorList(
                [u'Comment with this author and movie already exists.']
            )
            return False

        return True

    def clean_user_pk(self):
        user_pk = self.cleaned_data['user_pk']
        if not User.objects.filter(pk=user_pk).exists():
            raise ValidationError('Invalid user_pk.')

        return user_pk

    def clean_movie_pk(self):
        movie_pk = self.cleaned_data['movie_pk']
        if not Movie.objects.filter(pk=movie_pk).exists():
            raise ValidationError('Invalid movie_pk.')

        return movie_pk
