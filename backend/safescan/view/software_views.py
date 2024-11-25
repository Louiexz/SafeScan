from .views import *
import vt
from ml_model.ai_model import make_prediction
from decouple import config

def transform_groups(data):
    # Mapeamento dos grupos de campos
    field_groups = {
        'localizacao_rede': [
            'ACCESS_COARSE_LOCATION','ACCESS_FINE_LOCATION','CHANGE_NETWORK_STATE','WAKE_LOCK'
        ],
        'bluetooth_funcionalidades': [
            'BLUETOOTH','SEND_SMS','RECEIVE_BOOT_COMPLETED','GET_TASKS'
        ],
        'arquivos_confOS': [
            'WRITE_EXTERNAL_STORAGE','SYSTEM_ALERT_WINDOW', 'DISABLE_KEYGUARD',
            'KILL_BACKGROUND_PROCESSES'
        ],
        'sms': [
            'READ_SMS','SEND_SMS','RECEIVE_SMS',
            'Landroid/telephony/SmsManager;->sendMultipartTextMessage'
        ],
        'midia_audio': [
            'VIBRATE','Landroid/media/AudioRecord;->startRecording'
        ],
        'camera': [
            'Landroid/location/LocationManager;->getLastKgoodwarewnLocation',
            'Landroid/telephony/TelephonyManager;->getCellLocation'
        ],
        'rede_operadora': [
            'Landroid/telephony/TelephonyManager;->getNetworkCountryIso',
            'Landroid/telephony/TelephonyManager;->getNetworkOperator',
            'Landroid/telephony/TelephonyManager;->getNetworkOperatorName',
        ],
        'sim_pais': [
            'Landroid/telephony/TelephonyManager;->getSimOperator',
            'Landroid/telephony/TelephonyManager;->getSimCountryIso',
            'Landroid/telephony/TelephonyManager;->getSimOperatorName'
        ],
        'biblioteca_class': [
            'Ljava/lang/System;->load', 'Ljava/lang/System;->loadLibrary',
            'Ldalvik/system/DexClassLoader;->loadClass','Ljava/net/URL;->openConnection'
        ],
        'pacotes': [
            'Landroid/content/pm/PackageManager;->getInstalledPackages'
        ]
    }

    software = {}  # Dicionário para armazenar os valores dos campos

    # Iterando sobre os grupos de campos
    for group, fields in field_groups.items():
        group_value = data.get(group)
        
        # Se o campo do grupo não existir, podemos registrar um erro ou simplesmente continuar
        if group_value is None: return {"erro":True}
        
        # Atribui o valor ao campo correspondente
        for field in fields: software[field] = group_value

    return software  # Retorna o dicionário com os valores atribuídos

class SoftwareFormBase(APIView):
    def handle_software_creation(self, request, is_authenticated):
        # Criação do serializer
        serializer = CreateSoftwareSerializer(data=request.data)

        if serializer.is_valid():
            # Adiciona o usuário aos dados (None para não autenticados)
            if is_authenticated:
                serializer.validated_data["user"] = request.user
            else:
                serializer.validated_data["user"] = None

            # Salva a instância do modelo
            software_instance = serializer.save()

            # Converte os dados para o formato adequado para o modelo de predição
            software_data = transform_groups(request.data)

            # Verifica se há erro nos dados
            try:
                software_data['erro']
                return Response({
                    "message": """
                        Dados inválidos. Inclua 'name', 'localizacao_rede', 'bluetooth_funcionalidades',
                        'arquivos_confOS', 'sms',' midia_audio', 'camera', 'rede_operadora', 'sim_pais', 'biblioteca_class',
                        'pacotes' para criar um software.
                    """
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception: pass

            # Fazendo a predição com o modelo de IA
            prediction = make_prediction(software_data)

            # Atualiza o campo 'label' com a predição
            software_instance.label = prediction
            software_instance.save()

            return Response({
                "message": "Software criado com sucesso.", "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": """Dados inválidos. Inclua 'name', 'localizacao_rede', 'bluetooth_funcionalidades',
                'arquivos_confOS', 'sms',' midia_audio', 'camera', 'rede_operadora', 'sim_pais', 'biblioteca_class',
                'pacotes' para criar um software."""
            }, status=status.HTTP_400_BAD_REQUEST)

class software_form_auth(SoftwareFormBase):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return self.handle_software_creation(request, is_authenticated=True)

class software_form_unauth(SoftwareFormBase):
    def post(self, request):
        return self.handle_software_creation(request, is_authenticated=False)

class view_software(APIView):
    def get(self, request):
        softwareData = Software.objects.all()
        serializer = GetSoftwareSerializer(softwareData, many=True)
        return Response({"message": "All softwares data.", "data": serializer.data},
                        status=status.HTTP_200_OK)

class view_url_file(APIView):
    def get(self, request):
        return Response({"message": "Check software by: url or file}"}, 
                        status=status.HTTP_200_OK)

    def post(self, request):
        if request.data.get("file") or request.data.get("url"):
            try:
                client = vt.Client(config("API_KEY"))
            except Exception as e:
                return Response({"message": "Not connected with VirusTotal's API."},
                                status=status.HTTP_400_BAD_REQUEST)

            if request.data.get("file"):
                file_name = request.data.get("file")
                try:
                    file = client.get_object(f"/files/{file_name}")
                    return Response({"message": "File uploaded.", "data": file.to_dict()},
                                    status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"message": "Error retrieving file.", "error": str(e)},
                                    status=status.HTTP_400_BAD_REQUEST)

            elif request.data.get("url"):
                url = request.data.get("url")
                url_id = vt.url_id(url)
                try:
                    url_data = client.get_object(f"/urls/{url_id}")
                    return Response({"message": "URL searched.", "data": url_data.last_analysis_stats},
                                    status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"message": "Error retrieving URL.", "error": str(e)},
                                    status=status.HTTP_400_BAD_REQUEST)

class delete_software(APIView):
    def delete(self, request, id):
        try:
            # Busca o software pelo UUID
            software = Software.objects.get(id=id)
            software.delete()
            return Response({"message": "Software deleted."}, status=status.HTTP_200_OK)
        except Software.DoesNotExist:
            return Response({"error": "Software not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error deleting software."}, status=status.HTTP_400_BAD_REQUEST)
