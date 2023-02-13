from django.contrib.auth.decorators import login_required
from django.urls import path

from movies.views import MovieListView, MovieView, SuggestionsMoviesView

app_name = 'movies'
urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('detail/<pk>/', MovieView.as_view(), name='movie_detail'),
    path('suggestions/', login_required(SuggestionsMoviesView.as_view()), name='suggestions'),
]
