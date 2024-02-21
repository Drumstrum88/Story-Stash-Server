from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from storystashapi.models.book import Book
from storystashapi.models.genre import Genre
from storystashapi.serializers.bookSerializer import BookSerializer

class BookView(ViewSet):
  """Book View"""
  
  """Handles GET request for single book"""
  
  def retrieve(self, request, pk):
    try:
      book = Book.objects.get(pk=pk)
      serializer = BookSerializer(book)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Book.DoesNotExist as ex:
      return Response({'message' : ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    
  """Handles Get request for all books"""
  def list(self, request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)
  
  
  """Handles POST request for a new book"""
  def create(self, request):
    genre = Genre.objects.get(pk=request.data.get('genre_id'))
    
    book = Book.objects.create(
      genre = genre,
      title=request.data.get('title'),
      description=request.data.get('description')
      
    )

    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  
  """Handles PUT for a book"""
  def update(self, request, pk):
    try:
      book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
      return Response({'error': "Book Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
    
    genre = Genre.objects.get(pk=request.data.get('genre', book.genre.pk))
    
    book.genre = genre
    
    if 'title' in request.data:
      book.title = request.data['title']
      
    if 'description' in request.data:
      book.description = request.data['description']
      
    book.save()
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  
  """Handles DELETE for book"""
  def destroy(self, request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
