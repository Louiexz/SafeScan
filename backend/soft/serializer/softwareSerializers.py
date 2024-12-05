from rest_framework import serializers

from ..model import Software, User

class ProfileSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Software
        fields=["id", "name", "label", 'localizacao', 'rede', 'bluetooth', 'armazenamento',
                  'sistema', 'message', 'midia_audio', 'biblioteca_classes', 'pacotes', "created_at", "updated_at"]

class GetSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Software
        fields=["name", "label", "created_at", "updated_at"]

class CreateSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software
        fields = ["name", "localizacao", "rede", "bluetooth", "armazenamento",
                  "sistema", "message", "midia_audio", "biblioteca_classes", "pacotes"]

    def validate_name(self, value):
        """
        Validação customizada para garantir que o nome do software seja único.
        """
        if Software.objects.filter(name=value).exists():
            raise serializers.ValidationError("Este nome de software já está em uso.")
        return value

class UpdateSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software
        fields = ['name', 'localizacao', 'rede', 'bluetooth', 'armazenamento',
                  'sistema', 'message', 'midia_audio', 'biblioteca_classes', 'pacotes']
    
    def validate_name(self, value):
        """
        Validação customizada para garantir que o nome do software seja único.
        """
        # Verifica se o software com o nome já existe no banco de dados
        if Software.objects.filter(name=value).exists():
            raise serializers.ValidationError("Este nome de software já está em uso.")
        return value
