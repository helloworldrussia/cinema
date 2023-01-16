from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

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
            self.create_comment()
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
            if settings.DEBUG:
                raise ValidationError('Comment with this author and movie already exists')
