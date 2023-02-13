from django.db.models import Q, IntegerField, Value, When, Case

from movies.models import Movie


class BaseSuggestionsView:
    recommender = None

    def get_queryset(self):
        queryset = self.recommender.get_suggestions()

        return queryset


class Recommender:

    def get_suggestions(self):
        raise NotImplementedError()


class MovieRecommender(Recommender):
    user = None

    def get_suggestions(self):
        if not self.user:
            return Movie.objects.all()

        request_params = self.get_request_params()

        queryset = Movie.objects.exclude(
            pk__in=request_params['unloved_movies_pks']
        ).annotate(
            display_priority=Case(
                When(request_params['q_list'], then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by(
            '-display_priority'
        ).distinct()

        return queryset

    def get_request_params(self):
        unloved_movies_pks = self.get_unloved_movies()

        liked_movies = Movie.objects.filter(
            comment__author=self.user,
            comment__rate__gt=3
        )

        filters_params = self.get_filters_params(liked_movies)
        q_list = self.get_suggestions_filters(filters_params)

        request_params = {
            'q_list': q_list,
            'unloved_movies_pks': unloved_movies_pks
        }

        return request_params

    def get_unloved_movies(self):
        disliked_movies = Movie.objects.filter(
            comment__author=self.user,
            comment__rate__lte=3
        )

        filters_params = self.get_filters_params(disliked_movies)
        q_list = self.get_suggestions_filters(filters_params)

        unloved_movies = Movie.objects.filter(q_list).values_list('pk')

        return unloved_movies

    @staticmethod
    def get_suggestions_filters(filters_params):
        filters = Q(
            actors__in=filters_params['actors']
        ) | Q(
            genre__in=filters_params['genre']
        ) | Q(
            director__in=filters_params['director']
        )

        return filters

    @staticmethod
    def get_filters_params(queryset):
        params = {
            'actors': queryset.values_list('actors', flat=True),
            'genre': queryset.values_list('genre', flat=True),
            'director': queryset.values_list('director', flat=True)
        }

        return params
