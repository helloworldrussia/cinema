from django.urls import path

from movies.views import MovieListView, MovieView

app_name = 'movies'
urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('detail/<pk>/', MovieView.as_view(), name='movie_detail')
]