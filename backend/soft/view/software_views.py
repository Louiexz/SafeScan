from .views import *
import vt
from ml_model.ai_model import make_prediction
from decouple import config

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
            software_data = serializer.validate(request.data)

            # Verifica se há erro nos dados
            try:
                software_data['erro']
                return Response({
                    "message": """
Dados inválidos. Inclua 'name', 'localizacao', 'rede', 'bluetooth', 'armazenamento', 'sistema',
'message', 'midia_audio', 'biblioteca_classes', 'pacotes' para criar um software.
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
                "message": """
Dados inválidos. Inclua 'name', 'localizacao', 'rede', 'bluetooth', 'armazenamento', 'sistema',
'message', 'midia_audio', 'biblioteca_classes', 'pacotes' para criar um software."""
            }, status=status.HTTP_400_BAD_REQUEST)

class SoftwareFormAuth(SoftwareFormBase):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create software authenticated",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the software"),
                'localizacao_rede': openapi.Schema(type=openapi.TYPE_STRING, description="Network location of the software"),
                'bluetooth_funcionalidades': openapi.Schema(type=openapi.TYPE_STRING, description="Bluetooth functionalities"),
                'arquivos_confOS': openapi.Schema(type=openapi.TYPE_STRING, description="Configuration files for OS"),
                'sms': openapi.Schema(type=openapi.TYPE_STRING, description="SMS functionalities"),
                'midia_audio': openapi.Schema(type=openapi.TYPE_STRING, description="Audio media functionalities"),
                'camera': openapi.Schema(type=openapi.TYPE_STRING, description="Camera functionalities"),
                'rede_operadora': openapi.Schema(type=openapi.TYPE_STRING, description="Carrier network"),
                'sim_pais': openapi.Schema(type=openapi.TYPE_STRING, description="SIM country"),
                'biblioteca_class': openapi.Schema(type=openapi.TYPE_STRING, description="Class library"),
                'pacotes': openapi.Schema(type=openapi.TYPE_STRING, description="Packages used by the software"),
            },
            required=['name', 'localizacao', 'rede', 'bluetooth',
                      'armazenamento', 'sistema', 'message', 'midia_audio',
                      'biblioteca_classes'],  # Defining the mandatory fields for software creation
        ),
        responses={
            200: openapi.Response(
                description="Software created successfully",
                examples={
                    'application/json': {
                        "message": "The software has been successfully created."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid data",
                examples={
                    'application/json': {
                        "error": "Invalid data provided. Please check the required fields."
                    }
                }
            ),
        },
        tags=["Software"]
    )
    def post(self, request):
        return self.handle_software_creation(request, is_authenticated=True)

class SoftwareFormUnauth(SoftwareFormBase):
    @swagger_auto_schema(
            
        operation_description="Create software unauthenticated",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the software"),
                'localizacao': openapi.Schema(type=openapi.TYPE_STRING, description="Network location of the software"),
                'rede': openapi.Schema(type=openapi.TYPE_STRING, description="Carrier network"),
                'bluetooth': openapi.Schema(type=openapi.TYPE_STRING, description="Bluetooth functionalities"),
                'armazenamento': openapi.Schema(type=openapi.TYPE_STRING, description="Camera functionalities"),
                'sistema': openapi.Schema(type=openapi.TYPE_STRING, description="Configuration functions or OS"),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="SMS functionalities"),
                'midia_audio': openapi.Schema(type=openapi.TYPE_STRING, description="Media functionalities and vibration"),
                'biblioteca_classes': openapi.Schema(type=openapi.TYPE_STRING, description="SIM country"),
                'pacotes': openapi.Schema(type=openapi.TYPE_STRING, description="Packages used by the software"),
            },
            required=['name', 'localizacao', 'rede', 'bluetooth',
                      'armazenamento', 'sistema', 'message', 'midia_audio',
                      'biblioteca_classes'],  # Defining the mandatory fields for software creation
        ),
        responses={
            200: openapi.Response(
                description="Software created successfully",
                examples={
                    'application/json': {
                        "message": "The software has been successfully created.",
                        "software_id": 123,  # Example response with software ID
                        "name": "Example Software"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid data",
                examples={
                    'application/json': {
                        "error": "Invalid data provided. Please check the required fields."
                    }
                }
            ),
        },
        tags=["Software"]
    )
    def post(self, request):
        return self.handle_software_creation(request, is_authenticated=False)

class ViewSoftware(APIView):
    @swagger_auto_schema(
        operation_description="Get all software data",
        request_body=None,  # Não é necessário corpo na requisição para uma operação GET
        responses={
            200: openapi.Response(
                description="List of all software",
                examples={
                    'application/json': {
                        "message": "Successfully fetched all software data",
                        "software": [
                            {"name": "Software A", "Status": "Goodware"},
                            {"name": "Software B", "Status": "Malware"}
                        ]
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid parameters",
                examples={
                    'application/json': {
                        "error": "Invalid request parameters."
                    }
                }
            ),
        },
        tags=["Software"]
    )
    def get(self, request):
        softwareData = Software.objects.all()
        serializer = GetSoftwareSerializer(softwareData, many=True)
        return Response({"message": "All softwares data.", "data": serializer.data},
                        status=status.HTTP_200_OK)

class ViewUrlFile(APIView):
    @swagger_auto_schema(
        operation_description="Check software by URL or file",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'url': openapi.Schema(type=openapi.TYPE_STRING, description='URL for the software to check'),
                'file': openapi.Schema(type=openapi.TYPE_STRING, description='File to check for the software'),
            },
            required=[],  # Fields are optional in the request body
        ),
        responses={
            200: openapi.Response(
                description="Software check completed successfully",
                examples={
                    'application/json': {
                        "message": "The software has been successfully checked."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid data",
                examples={
                    'application/json': {
                        "error": "Either 'url' or 'file' must be provided for the software check."
                    }
                }
            ),
        },
        tags=["Software"]
    )
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

class UpdateSoftware(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update software by ID",
        request_body=None,  # Não é necessário corpo na requisição para deletar
        responses={
            204: openapi.Response(
                description="Software updated successfully",
                examples={
                    'application/json': {
                        "message": "The software has been successfully updated."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid data",
                examples={
                    'application/json': {
                        "error": "Invalid software ID or missing parameters."
                    }
                }
            ),
            404: openapi.Response(
                description="Software not found",
                examples={
                    'application/json': {
                        "error": "Software with the given ID does not exist."
                    }
                }
            ),
        },
        tags=["Software"]
    )
    def put(self, request, id):
        try:
            software = Software.objects.get(pk=id)
        except Software.DoesNotExist:
            return Response({"error": "Software not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateSoftwareSerializer(software, data=request.data, partial=True)

        if serializer.is_valid():
            software_instance = serializer.save()
            
            software_data = serializer.validate(request.data)

            # Verifica se há erro nos dados
            try:
                software_data['erro']
                return Response({
                    "message": """
Dados inválidos. Inclua 'name', 'localizacao', 'rede', 'bluetooth', 'armazenamento', 'sistema',
'message', 'midia_audio', 'biblioteca_classes', 'pacotes' para criar um software.
                    """
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception: pass

            # Fazendo a predição com o modelo de IA
            prediction = make_prediction(software_data)

            software_instance.label = prediction

            serializer.save()
            return Response({"message": "Software updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteSoftware(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Delete software by ID",
        request_body=None,  # Não é necessário corpo na requisição para deletar
        responses={
            204: openapi.Response(
                description="Software deleted successfully",
                examples={
                    'application/json': {
                        "message": "The software has been successfully deleted."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid data",
                examples={
                    'application/json': {
                        "error": "Invalid software ID or missing parameters."
                    }
                }
            ),
            404: openapi.Response(
                description="Software not found",
                examples={
                    'application/json': {
                        "error": "Software with the given ID does not exist."
                    }
                }
            ),
        },
        tags=["Software"]
    )
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
