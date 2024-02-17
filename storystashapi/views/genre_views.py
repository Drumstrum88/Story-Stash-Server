from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import serializers

from storystashapi.models.genre import Genre
from storystashapi.serializers.genreSerializer import GenreSerializer

class GenreView(ViewSet):
  """Genre View"""
  
  """Handles GET for single genre"""
  def retrieve(self, request, pk):
    try:
      genre = Genre.objects.get(pk=pk)
      serializer = GenreSerializer(genre)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Genre.DoesNotExist as ex:
      return  Response({'mesage' : ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


  """Handles GET request for all genres"""
  def list(self, request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)
