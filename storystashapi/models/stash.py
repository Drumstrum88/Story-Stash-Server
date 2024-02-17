from django.db import models

from storystashapi.models.user import User

class Stash(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
  title = models.CharField(max_length=25)
