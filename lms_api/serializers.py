from rest_framework import serializers
from .models import Library, LibraryUser

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = '__all__'
    
    def create(self, validated_data):
        return LibraryUser.objects.create_user(**validated_data)
