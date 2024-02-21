from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from storystashapi.models.book import Book
from storystashapi.models.stash import Stash
from storystashapi.models.stash_book import StashBook
from storystashapi.serializers.stashBookSerializer import StashBookSerializer

class StashBookView(ViewSet):
  """Stash View"""
  
  """Handles GET request for a single stash book"""
  def retrieve(self, request, pk):
    try:
      stash_book = StashBook.objects.get(pk=pk)
      serializer = StashBookSerializer(stash_book)
      return Response(serializer.data)
    except StashBook.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    
  """Handles GET request for all stash books"""
  def list(self, request):
    stash_book = StashBook.objects.all()
    serializer = StashBookSerializer(stash_book, many=True)
    return Response(serializer.data)
  
  
  """Handles POST request for a stash book"""
  def create(self, request):
    stash = Stash.objects.get(pk=request.data['stash_id'])
    book = Book.objects.get(pk=request.data['book_id'])
    
    stash_book = StashBook.objects.create(
      stash=stash,
      book=book
    )
    
    serializer = StashBookSerializer(stash_book)
    return Response(serializer.data)
  
  
  """Handles DELETE request for stash book"""
  def destroy(self, request, pk):
    stash_book = StashBook.objects.get(pk=pk)
    stash_book.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
