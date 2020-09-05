from django.contrib.auth import get_user_model
from rest_framework import serializers
from movies.models import Rate


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','is_superuser','is_staff','is_active','rates','karma')