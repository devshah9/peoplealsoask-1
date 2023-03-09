from paa.models import KeyWordOfPaa, KeyWordAnswer, KeyWordRelated, KeyWordImages, KeyWordVideos, KeyWordGoogleImages
from rest_framework import serializers


class KeyWordAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWordAnswer
        fields = ['question', 'answer']


class KeyWordOfPaaSerializer(serializers.ModelSerializer):
    result = KeyWordAnswerSerializer(many=True, read_only=True)
    related_search = serializers.StringRelatedField(many=True, read_only=True)
    images = serializers.StringRelatedField(many=True, read_only=True)
    youtube_videos = serializers.StringRelatedField(many=True, read_only=True)
    google_images = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = KeyWordOfPaa
        fields = ['id', 'keyword', 'numoftimes', 'related_search', 'result', 'images', 'youtube_videos', 'google_images']


class KeyWordRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWordRelated
        fields = '__all__'


class KeyWordImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWordImages
        fields = '__all__'


class KeyWordVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWordVideos
        fields = '__all__'


class KeyWordGoogleImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWordGoogleImages
        fields = '__all__'
