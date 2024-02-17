from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from storystashapi.models.genre import Genre

class GenreSerializer(serializers.ModelSerializer):
  
  class Meta:
    model: Genre
    fields = ('id', 'label')
    
