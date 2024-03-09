from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from storystashapi.models.book import Book
from storystashapi.models.genre import Genre
from storystashapi.models.user import User
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
    genre = Genre.objects.get(pk=request.data.get('genre'))
    image_url = request.data.get('image')
    user = User.objects.get(uid=request.data['uid'])
    
    book = Book.objects.create(
      genre = genre,
      title=request.data.get('title'),
      description=request.data.get('description'),
      image=image_url,
      user=user,
      
    )

    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  
  """Handles PUT for a book"""
  def update(self, request, pk):
    try:
        print(f"Received book update request for pk: {pk}")
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': "Book Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        print('Request data:', request.data)
        genre_id = int(request.data.get('genre_id'))
        genre = Genre.objects.get(pk=genre_id)
    except (ValueError, Genre.DoesNotExist):
        return Response({'error': "Invalid or non-existent genre_id"}, status=status.HTTP_400_BAD_REQUEST)

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


  """Handles GET for books filtered by Genre"""

  @action(detail=False, methods=['GET'])
  def list_filtered_by_genre(self, request):
      selected_genre_id = request.query_params.get('genre', None)


      if selected_genre_id:
          books = Book.objects.filter(genre_id=selected_genre_id)
      else:
          books = Book.objects.all()

      serializer = BookSerializer(books, many=True)
      return Response(serializer.data)


@api_view(['GET'])
def search_books(request):
    query = request.query_params.get('query', '')

    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)
