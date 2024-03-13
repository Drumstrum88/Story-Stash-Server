from django.http import HttpResponseServerError, JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from storystashapi.models.book import Book

from storystashapi.models.review import Review
from storystashapi.models.user import User
from storystashapi.serializers.review_serializer import ReviewSerializer

class ReviewView(ViewSet):
  
  def retrieve(self, request, pk):
    """Handles GET request for a single review"""
    
    try:
      review = Review.objects.get(pk=pk)
      serializer = ReviewSerializer(review)
      return Response(serializer.data)
    except Book.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    
  def list(self, request, book_id):
      try:
          print(request.data)
          reviews = Review.objects.filter(book_id=book_id)
          serializer = ReviewSerializer(reviews, many=True)
          return Response(serializer.data)
      except Book.DoesNotExist:
          return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

  
  
  def post(self, request):
    """Handles POST request for a review"""
    try:
      print(request.data)
      uid = request.data.get('uid', None)
      book_id = request.data.get('book', None)
      content = request.data.get('content', None)
      
      user =User.objects.get(uid=uid)
      book = Book.objects.get(pk=book_id)
      
      review = Review.objects.create(
        content=content,
        book=book,
        user=user,
      )
      
      serializer = ReviewSerializer(review)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
      return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  
  def update(self, request, pk):
    """Handles PUT request for updating a review"""
    try:
        review = Review.objects.get(pk=pk)
        content = request.data.get('content')
        if content:
            review.content = content
            review.save()
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

  
  
  def destroy(self, request, pk):
    """Handles Delete request for a review"""
    print(request.data)
    review = Review.objects.get(pk=pk)
    review.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
