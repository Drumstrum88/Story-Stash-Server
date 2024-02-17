from django.db import models
from storystashapi.models.book import Book
from storystashapi.models.stash import Stash

from storystashapi.models.user import User

class StashBook(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
  stash = models.ForeignKey(Stash, on_delete=models.CASCADE, default=None)
  book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
