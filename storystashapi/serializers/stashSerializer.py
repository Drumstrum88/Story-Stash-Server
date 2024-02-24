from rest_framework import serializers
from storystashapi.models.stash import Stash
from storystashapi.serializers.stashBookSerializer import StashBookSerializer

class StashSerializer(serializers.ModelSerializer):
  books = StashBookSerializer(many=True, read_only=True)
  
  class Meta:
    model = Stash
    fields = ('id', 'user', 'title', 'books',)
    depth = 2
    
