from django.db.models import Avg, Case, When, Value, IntegerField, Count, Prefetch
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from authentication.models import User
from movies.filters import MovieFilterSet
from movies.forms import MovieFilterSearchForm, MovieCommentForm
from movies.models import Movie


class MovieListView(ListView):
    queryset = Movie.objects.values('pk', 'title', 'poster')
    template_name = 'movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered = MovieFilterSet(self.request.GET, queryset)

        return filtered.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MovieFilterSearchForm

        return context


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
