from rest_framework import serializers

from storystashapi.models.review import Review
from storystashapi.serializers.userSerializer import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  
  class Meta:
    model = Review
    fields = ('id', 'content', 'user', 'date', 'book')
    depth = 1
