from django.core.exceptions import ValidationError
from django.db import models


class BaseMovieDetail(models.Model):
    name = models.CharField(max_length=155)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Director(BaseMovieDetail):
    pass


class Actor(BaseMovieDetail):
    pass


class Genre(BaseMovieDetail):
    pass


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    director = models.ForeignKey(Director, null=True, blank=True, on_delete=models.SET_NULL)
    actors = models.ManyToManyField(Actor, null=True, blank=True)
    genre = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.pk} | {self.title}"


class Comment(models.Model):
    RATING_CHOICES = (
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐')
    )
    movie = models.ForeignKey(Movie, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f"{self.pk} | {self.author}"

    def validate_unique(self, exclude=None):
        if Comment.objects.filter(author=self.author, movie=self.movie).exists():
            raise ValidationError('Comment with this author and movie already exists')

        super(Comment, self).validate_unique(exclude=exclude)

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Comment, self).save(*args, **kwargs)
