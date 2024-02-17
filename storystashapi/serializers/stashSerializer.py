from rest_framework import serializers
from storystashapi.models.stash import Stash

class StashSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Stash
    fields = ('id', 'user_id', 'title')
    depth = 1
    
