from django.contrib import admin

from movies.models import Movie, Comment, Actor, Director, Genre

admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Genre)

