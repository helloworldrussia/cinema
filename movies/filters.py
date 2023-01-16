from django.db.models import Q
from django_filters import FilterSet, CharFilter, Filter

from movies.models import Movie


class MovieFilterSet(FilterSet):
    search = CharFilter(method='filter_search')
    genres = Filter(method='filter_genres')

    class Meta:
        model = Movie
        fields = ('actors', 'director', 'genre')

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(
                title__icontains=value
            ) | Q(
                description__icontains=value
            ) | Q(
                actors__name__icontains=value
            ) | Q(
                director__name__icontains=value
            )
        ).distinct()

    def filter_genres(self, queryset, name, value):
        return queryset.filter(genre=value)
