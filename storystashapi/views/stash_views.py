from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import serializers

from storystashapi.models.stash import Stash
from storystashapi.models.stash_book import StashBook
from storystashapi.models.user import User
from storystashapi.serializers.stashBookSerializer import StashBookSerializer
from storystashapi.serializers.stashSerializer import StashSerializer

class StashView(ViewSet):
  """Stash View"""
  
  """Handles GET request for a single stash"""
  def retrieve(self, request, pk):
    try:
      stash = Stash.objects.get(pk=pk)
      serializer = StashSerializer(stash)
      return Response(serializer.data, status.HTTP_200_OK)
    except Stash.DoesNotExist as ex:
      return Response({'message' : ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    
  """Handle GET requests for all Genres"""
  def list(self, request):
    
    try:
      uid = request.query_params['uid']
      user = User.objects.get(uid=uid)
      stashes = Stash.objects.filter(user=user.id)
      serializer = StashSerializer(stashes, many=True)
      return Response(serializer.data)
    except:
      stashes = Stash.objects.all()
      serializer = StashSerializer(stashes, many=True)
      return Response(serializer.data)
    
  
  """Handles POST request for a stash"""
  def create(self, request):
    user = User.objects.get(pk=request.data.get('user_id'))
    
    stash = Stash.objects.create(
      user=user,
      title=request.data.get('title')
    )
    
    serializer = StashSerializer(stash)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  
  """Handles PUT for a stash"""
  def update(self, request, pk):
    try:
      stash = Stash.objects.get(pk=pk)
    except Stash.DoesNotExist:
      return Response({'error': "stash does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    user_id = User.objects.get(pk=request.data.get('user_id'))
    
    stash.user_id = user_id
    
    if 'title' in request.data:
      stash.title = request.data['title']
      
    stash.save()
    serializer = StashSerializer(stash)
    return Response(serializer.data, status=status.HTTP_200_OK)


"""Handles DELETE for a stash"""
def destroy (self, request, pk):
  stash = Stash.objects.get(pk=pk)
  stash.delete()
  return Response(None, status=status.HTTP)


"""Method to get all books associated with a single stash"""
@action(methods=['get'], detail=True)
def books(self, request, pk):
  book = StashBook.objects.all()
  books = book.filter(stash_id=pk)
  
  serializer = StashBookSerializer(books, many=True)
  return Response(serializer.data)
  
