from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Movie,Genre,Rate

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name','id')


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True,read_only=True)
    # like_users = UserSerializer(read_only=True,required=False)
    # visited_users = UserSerializer(read_only=True,required=False)
    class Meta:
        model = Movie
        # fields = ('title','release_date','overview','vote_count','vote_average','genres','popularity','poster_path',)
        # fields='__all__'
        exclude = ('like_users','visited_users')



class RateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Rate
        fields = '__all__'




