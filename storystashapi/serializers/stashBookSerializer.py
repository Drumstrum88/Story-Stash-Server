from rest_framework import serializers
from storystashapi.models.stash_book import StashBook
from storystashapi.serializers.userSerializer import UserSerializer

class StashBookSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    isRead = serializers.BooleanField()
    
    class Meta:
        model = StashBook
        fields = ['id', 'stash', 'book', 'user', 'isRead']
        depth = 6


    
