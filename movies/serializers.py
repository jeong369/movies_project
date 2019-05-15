from rest_framework import serializers
from .models import Movie, Score

        
class MovieSerializer(serializers.ModelSerializer):
    expected_score = serializers.FloatField(default=0)
    class Meta:
        model = Movie
        fields = ('id', 'pk', 'title', 'en_title', 'genres', 'open_date', 'director', 'actors', 'rated', 'summary', 'imageurl', 'hashtags', 'score_users', 'expected_score',)

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('grade',)

