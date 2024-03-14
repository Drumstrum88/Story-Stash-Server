from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from storystashapi.models.book import Book
from storystashapi.models.stash import Stash
from storystashapi.models.stash_book import StashBook
from storystashapi.models.user import User
from storystashapi.serializers.stashBookSerializer import StashBookSerializer
from rest_framework.permissions import IsAuthenticated


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
    stash_books = StashBook.objects.all()
    serializer = StashBookSerializer(stash_books, many=True)
    return Response(serializer.data)

  
  
  """Handles POST request for a stash book"""
  def post(self, request):
        stash = Stash.objects.get(pk=request.data['stash'])
        book_ids = request.data.get('books', [])

        stash_books = []
        if isinstance(book_ids, list):
            for book_id in book_ids:
                try:
                    book = Book.objects.get(pk=book_id)
                    stash_book = StashBook.objects.create(
                        stash=stash,
                        book=book,
                        isRead=False,
                        user=stash.user
                    )
                    stash_books.append(stash_book)
                except Book.DoesNotExist:
                    print(f"Book with ID {book_id} does not exist.")
        elif isinstance(book_ids, int):
            try:
                book = Book.objects.get(pk=book_ids)
                stash_book = StashBook.objects.create(
                    stash=stash,
                    book=book,
                    isRead=False,
                    user=stash.user
                )
                stash_books.append(stash_book)
            except Book.DoesNotExist:
                print(f"Book with ID {book_ids} does not exist.")

        serializer = StashBookSerializer(stash_books, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


  def update(self, request, pk):
        """Handles PUT request for stashbook"""
        stash_book = StashBook.objects.get(pk=pk)
        
        try:
            stash_book.stash = Stash.objects.get(pk=request.data["stash"])
        except Stash.DoesNotExist:
            return Response({"error": "Invalid Stash ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        book_id = request.data["book"]["id"]
        try:
            book_instance = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Invalid Book ID"}, status=status.HTTP_400_BAD_REQUEST)

        stash_book.book = book_instance
        stash_book.isRead = request.data["isRead"]
        
        stash_book.save()
        
        serializer = StashBookSerializer(stash_book, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

  
  
  """Handles DELETE request for stash book"""
  def destroy(self, request, pk):
    stash_book = StashBook.objects.get(pk=pk)
    stash_book.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  action(detail=False, methods=['GET'])
  def get_books_for_stash(self, request, stash_id=None):
        try:
            stash = get_object_or_404(Stash, pk=stash_id)
            stash_books = StashBook.objects.filter(stash=stash)
            serializer = StashBookSerializer(stash_books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Stash.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def get_read_books_for_user(self, request):
        try:
            user_id = request.GET.get('user_id', None)
            if user_id:
                user = get_object_or_404(User, pk=user_id)
                read_stash_books = StashBook.objects.filter(user=user, isRead=True)
                serializer = StashBookSerializer(read_stash_books, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User ID parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
