import json
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
    
    
  """Handle GET requests for all Stashes"""
  def list(self, request):
    
    stashes = Stash.objects.all()
    
    uid = request.query_params.get('uid')
    if uid is not None:
      user = User.objects.get(uid=uid)
      stashes= Stash.objects.filter(user=user.id)
    
    serializer = StashSerializer(stashes, many=True)
    return Response(serializer.data)
    
  
  """Handles POST request for a stash"""
  def create(self, request):
    try:
        user_uid = request.data.get('user')
        user = User.objects.get(uid=user_uid)
        
        stash = Stash.objects.create(
            user=user,
            title=request.data.get('title')
        )

        serializer = StashSerializer(stash)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except User.DoesNotExist:
        return Response({'error': "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    except KeyError as e:
        return Response({'error': f"KeyError: {e}"}, status=status.HTTP_400_BAD_REQUEST)



  
  
  """Handles PUT for a stash"""
  def update(self, request, pk):
    """Handles PUT requests for a stash"""
    
    user_uid = request.data.get('user')
    user = User.objects.get(uid=user_uid)
    
    stash = Stash.objects.get(pk=pk)
    
    stash.title = request.data['title']
    user = user
    
    
    stash.save()
    serializer = StashSerializer(stash)
    return Response(serializer.data, status=status.HTTP_200_OK)





  """Handles DELETE for a stash"""
  def destroy (self, request, pk):
    stash = Stash.objects.get(pk=pk)
    stash.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)


  """Method to get all books associated with a single stash"""
  @action(methods=['get'], detail=True)
  def books(self, request, pk):
    book = StashBook.objects.all()
    books = book.filter(stash_id=pk)
    
    serializer = StashBookSerializer(books, many=True)
    return Response(serializer.data)
  
