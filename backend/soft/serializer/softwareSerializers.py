from rest_framework import serializers

from ..model import Software, User

def transform_groups(data):
    # Mapeamento dos grupos de campos
    software = {}
    field_groups = {
        'localizacao': [
            'ACCESS_COARSE_LOCATION',
            'ACCESS_FINE_LOCATION',
            'Landroid/location/LocationManager;->getLastKgoodwarewnLocation',
            'Landroid/telephony/TelephonyManager;->getCellLocation',
            'Landroid/telephony/TelephonyManager;->getSimOperator',
            'Landroid/telephony/TelephonyManager;->getSimCountryIso',
            'Landroid/telephony/TelephonyManager;->getSimOperatorName',
            'Landroid/telephony/TelephonyManager;->getNetworkCountryIso',
            'Landroid/telephony/TelephonyManager;->getNetworkOperator',
            'Landroid/telephony/TelephonyManager;->getNetworkOperatorName',
        ],
        'rede':[
            'CHANGE_NETWORK_STATE',
            'Ljava/net/URL;->openConnection',
        ],
        'bluetooth': [
            'BLUETOOTH'
        ],
        'armazenamento':[
            'WRITE_EXTERNAL_STORAGE'
        ],
        'sistema': [
            'WAKE_LOCK',
            'RECEIVE_BOOT_COMPLETED',
            'GET_TASKS',
            'SYSTEM_ALERT_WINDOW',
            'DISABLE_KEYGUARD',
            'KILL_BACKGROUND_PROCESSES'
        ],
        'message': [
            'READ_SMS','SEND_SMS','RECEIVE_SMS',
            'Landroid/telephony/SmsManager;->sendMultipartTextMessage'
        ],
        'midia_audio': [
            'VIBRATE',
            'Landroid/media/AudioRecord;->startRecording'
        ],
        'biblioteca_classes': [
            'Ljava/lang/System;->load',
            'Ljava/lang/System;->loadLibrary',
            'Ldalvik/system/DexClassLoader;->loadClass',
        ],
        'pacotes': [
            'Landroid/content/pm/PackageManager;->getInstalledPackages'
        ]
    }

    # Iterando sobre os grupos de campos
    for group, fields in field_groups.items():
        group_value = data.get(group)
        
        # Se o campo do grupo não existir, podemos registrar um erro ou simplesmente continuar
        if group_value is None: return {"erro":True}
        
        # Atribui o valor ao campo correspondente
        for field in fields: software[field] = group_value

    return software  # Retorna o dicionário com os valores atribuídos

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

    def validate(self, data):
        """
        Transformações ou validações adicionais.
        """
        # Verifica se a função transform_groups está definida
        if "transform_groups" in globals():
            data = transform_groups(data)
        return data

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

    def validate(self, data):
        """
        Transformações ou validações adicionais.
        """
        # Verifica se a função transform_groups está definida
        if "transform_groups" in globals():
            data = transform_groups(data)
        return data