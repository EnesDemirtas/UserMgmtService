from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(**validated_data)
            return user
        except ValueError as e:
            raise serializers.ValidationError({'error': str(e)})
