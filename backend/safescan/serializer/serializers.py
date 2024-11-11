from rest_framework import serializers

from ..model import Software, User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label="Senha"
    )
    class Meta:
        model=User
        fields=["username, password"]
        extra_kwargs = {'password': {'write_only': True}}

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username", "email", "password"]
    
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        # Chama o método `create` da classe base
        return super().create(validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

class ProfileSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Software
        fields=["id", "name", "status", "created_at", "updated_at"]

class GetSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Software
        fields=["name", "status", "created_at", "updated_at"]

class CreateSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Software
        fields=["name", "status"]
