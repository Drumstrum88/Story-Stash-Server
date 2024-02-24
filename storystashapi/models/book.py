from django.db import models
from storystashapi.models.genre import Genre
from storystashapi.models.user import User


class Book(models.Model):
  title = models.CharField(max_length=25)
  genre = models.ForeignKey(Genre, on_delete=models.CASCADE, default= None)
  description = models.CharField(max_length=250, default=None)
  image =  models.CharField(max_length=400, default=None)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  
