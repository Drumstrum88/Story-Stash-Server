from rest_framework import serializers
from storystashapi.models.stash_book import StashBook
from storystashapi.serializers.bookSerializer import BookSerializer
from storystashapi.serializers.userSerializer import UserSerializer

class StashBookSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    isRead = serializers.BooleanField()
    book = BookSerializer(read_only=True)

    class Meta:
        model = StashBook
        fields = ['id', 'stash', 'book', 'user', 'isRead']
        depth = 1


    
