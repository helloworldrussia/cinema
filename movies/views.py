from django.db.models import Avg, Case, When, Value, IntegerField, Count, Prefetch, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from authentication.models import User
from movies.filters import MovieFilterSet
from movies.forms import MovieFilterSearchForm, MovieCommentForm
from movies.models import Movie


class BaseMovieListView(ListView):
    template_name = 'movie_list.html'
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MovieFilterSearchForm

        return context


class MovieListView(BaseMovieListView):
    queryset = Movie.objects.values('pk', 'title', 'poster')
    template_name = 'movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.request.GET)
        filtered = MovieFilterSet(self.request.GET, queryset)

        return filtered.qs


class MovieDetailView(DetailView):
    template_name = 'movie_detail.html'
    context_object_name = 'movie'

    def get_object(self, queryset=None):
        movie_pk = self.kwargs.get('pk')

        users_prefetch = Prefetch(
            'comment_set__author',
            queryset=User.objects.all().only('email')
        )

        movie = get_object_or_404(
            Movie.objects.select_related(
                'director', 'genre'
            ).prefetch_related(
                users_prefetch, 'actors', 'comment_set'
            ).annotate(
                rating=Avg('comment__rate'),
                commented=Count(
                    Case(
                        When(comment__author=self.request.user.pk,
                             then=Value(1)),
                        output_field=IntegerField()
                    )
                )
            ),
            pk=movie_pk
        )

        return movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial_data = {
            'user_pk': self.request.user.pk,
            'movie_pk': self.object.pk
        }
        context['form'] = MovieCommentForm(initial=initial_data)

        return context


class MovieCommentFormView(SingleObjectMixin, FormView):
    template_name = 'movie_detail.html'
    model = Movie
    form_class = MovieCommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('movies:movie_detail', kwargs={'pk': self.object.pk})


class MovieView(View):

    def get(self, request, *args, **kwargs):
        view = MovieDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = MovieCommentFormView.as_view()
        return view(request, *args, **kwargs)


class SuggestionsMoviesView(BaseMovieListView):

    def get_queryset(self):
        filters, viewed_pks = self.get_suggestions_filters()

        queryset = Movie.objects.exclude(
            pk__in=viewed_pks
        ).filter(filters).distinct()

        if not queryset:
            queryset = Movie.objects.all()

        return queryset

    def get_suggestions_filters(self):
        filters_params, viewed_pks = self.get_filters_params()
        filters = Q(
            actors__in=filters_params['actors']
        ) | Q(
            genre__in=filters_params['genre']
        ) | Q(
            director__in=filters_params['director']
        )

        return filters, viewed_pks

    def get_filters_params(self):
        params = {}

        queryset = Movie.objects.filter(
            comment__author=self.request.user,
            comment__rate__gt=3
        ).select_related(
            'genre', 'director'
        ).prefetch_related(
            'actors'
        )

        params['actors'] = queryset.values_list('actors', flat=True)
        params['genre'] = queryset.values_list('genre', flat=True)
        params['director'] = queryset.values_list('director', flat=True)

        viewed_pks = queryset.values_list('pk', flat=True)

        return params, viewed_pks
