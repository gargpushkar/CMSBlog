from django.db import models
from django.conf import settings
# Create your models here.


class MovieManager(models.Manager):
    def all_with_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')
        qs = qs.prefetch_related('writer', 'actors')
        return qs


class Movie(models.Model):
    """Model definition for Movie."""
    # TODO: Define fields here

    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, 'NR - Not Rated'),
        (RATED_G, 'G - General Audiences'),
        (RATED_PG, 'PG - Parental Guidance Suggested'),
        (RATED_R, 'R - Restricted'),
    )
    title = models.CharField(max_length=100)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)
    director = models.ForeignKey(
        to='Person',
        on_delete=models.SET_NULL,
        related_name='directed',
        null=True,
        blank=True
    )
    writer = models.ManyToManyField(
        to='Person',
        related_name='writing_credits',
        blank=True
    )
    actors = models.ManyToManyField(
        to='Person',
        through='Role',
        related_name='acting_credits',
        blank=True
    )
    objects = MovieManager()

    class Meta:
        """Meta definition for Movie."""

        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ('-year', 'title')

    def __str__(self):
        """Unicode representation of Movie."""
        return f'{self.title} ({self.year})'


class PersonManager(models.Manager):
    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed',
            'writing_credits',
            'role_set__movie'
        )


class Person(models.Model):
    """Model definition for Person."""
    # TODO: Define fields here

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)

    objects = PersonManager()

    class Meta:
        """Meta definition for Person."""

        verbose_name = 'Person'
        verbose_name_plural = 'Persons'
        ordering = ('first_name', 'last_name')

    def __str__(self):
        """Unicode representation of Person."""
        if self.died:
            return f'{self.first_name} {self.last_name} ({self.born}-{self.died})'
        return f'{self.first_name} {self.last_name} {self.born}'  # TODO


class Role(models.Model):
    """Model definition for Role."""
    # TODO: Define fields here
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)

    class Meta:
        """Meta definition for Role."""

        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        unique_together = ('movie', 'person', 'name')

    def __str__(self):
        """Unicode representation of Role."""
        return f'{self.movie_id} {self.person_id} {self.name}'  # TODO


class VoteManager(models.Manager):
    def get_vote_or_unsaved_blank_vote(self, movie, user):
        try:
            return Vote.objects.get(
                movie= movie,
                user= user
            )
        except Vote.DoesNotExist:
            return Vote(
                movie= movie,
                user= user
            )


class Vote(models.Model):
    """Model definition for Vote."""
    # TODO: Define fields here

    UP = 1
    DOWN = -1
    VALUE_CHOICES = {
        (UP, "👍",),
        (DOWN, "👎",),
    }
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    voted_on = models.DateField(auto_now=True)

    objects = VoteManager()

    class Meta:
        """Meta definition for Vote."""
        unique_together = ('user', 'movie')
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'

    def __str__(self):
        """Unicode representation of Vote."""
        pass
