from rest_framework import serializers
from storystashapi.models.user import User

class UserSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'uid')
