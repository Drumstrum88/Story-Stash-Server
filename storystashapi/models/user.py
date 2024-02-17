from django.db import models

class User(models.Model):
  first_name = models.CharField(max_length=25, default=None)
  last_name = models.CharField(max_length=25, default= None)
  uid = models.CharField(max_length=50, default=None)
