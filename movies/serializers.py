from rest_framework import serializers
from .models import Movie, Score
from accounts.models import User

        
class MovieSerializer(serializers.ModelSerializer):
    expected_score = serializers.FloatField(default=0)
    is_like = serializers.BooleanField(default=False)
    class Meta:
        model = Movie
        fields = ('id', 'pk', 'title', 'en_title', 'genres', 'open_date', 'director', 'actors', 'rated', 'summary', 'imageurl', 'hashtags', 'score_users', 'expected_score', 'is_like', )

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('grade',)


class UserSerializer(serializers.ModelSerializer):
    recommend_movies = MovieSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'recommend_movies',)
        
        