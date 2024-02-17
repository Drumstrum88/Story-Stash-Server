from rest_framework import serializers
from storystashapi.models.stash_book import StashBook

class StashBookSerializer(serializers.ModelSerializer):
  
  class Meta:
    model: StashBook
    fields = ['id', 'stash_id', 'book_id']
    depth = 1
    
