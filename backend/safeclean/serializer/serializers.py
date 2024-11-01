from rest_framework import serializers

from ..model import Software, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username", "password"]

class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Software
        fields=['name']