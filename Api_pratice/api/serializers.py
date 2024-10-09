from rest_framework.serializers import ModelSerializer
from to_do.models import Todo_List
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['id','username', 'email']

class Todo_ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo_List
        fields = '__all__'
    
    # Field-level validation for 'title'
    def validate_title(self, value):
        if not value.strip():  # Check if the title is empty or contains only whitespace
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value

    # Field-level validation for 'user'
    def validate_user(self, value):
        if value is None:
            raise serializers.ValidationError("User is required.")
        return value