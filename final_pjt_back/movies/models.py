from django.db import models
from django.conf import settings
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100)





class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField(default=False)
    overview = models.TextField()
    original_language = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=100)
    backdrop_path = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre)
    # rates = models.ManyToManyField(Rate)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    visited_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='visited_movies')



class Rate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="rates")