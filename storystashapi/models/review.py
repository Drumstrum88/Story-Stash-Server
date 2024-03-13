from django.db import models

from storystashapi.models.book import Book
from storystashapi.models.user import User

class Review(models.Model):
  content = models.TextField()
  book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateField(auto_now=True)
  
