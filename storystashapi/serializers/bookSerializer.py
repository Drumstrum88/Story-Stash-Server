from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from storystashapi.models.book import Book

class BookSerializer(serializers.ModelSerializer):
  stash = StashBookSerializer(many=True, read_only=True)
  
  class Meta:
    model = Book
    fields = ('id', 'title', 'genre_id', 'description')
    depth = 1
