from .views import *

from ..serializer import ProfileSerializer

class ViewProfile(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Get user data using token",
        request_body=None,  # O token é geralmente passado via header, não no corpo da requisição
        responses={
            200: openapi.Response(
                description="Profile data",
                examples={
                    'application/json': {
                        "message": "Successfully fetched user profile data",
                        "data": {
                            "name": "Random User",
                            "email": "youremail@example.com",
                            "softwares": [
                                {
                                    "name": "Software A",
                                    "status": "Goodware"
                                },
                                {
                                    "name": "Software B",
                                    "status": "Malware"
                                }
                            ]
                        }
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
            401: openapi.Response(
                description="Unauthorized, invalid or missing token",
                examples={
                    'application/json': {
                        "error": "Authentication token is missing or invalid."
                    }
                }
            ),
        },
        tags=["Profile"]
    )
    def get(self, request):
        # Ocultar a senha antes de serializar (não deve ser serializada)
        user_data = request.user
        user_data.password = "*****"  # Oculta a senha

        # Serializa os dados do usuário
        serializer = ProfileSerializer(user_data)
        
        # Recupera os softwares associados ao usuário
        softwareData = Software.objects.filter(user_id=request.user.id)
        softwareSerialize = ProfileSoftwareSerializer(softwareData, many=True)

        return Response({
            "message": "User profile data.",
            "data": serializer.data,
            "softwares": softwareSerialize.data
        }, status=status.HTTP_200_OK)

class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Update user data",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the user"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email address of the user"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password of the user (for update)"),
            },
            required=["name", "email"],  # Assuming 'name' and 'email' are required, 'password' is optional
        ),
        responses={
            200: openapi.Response(
                description="User profile updated successfully",
                examples={
                    'application/json': {
                        "message": "User profile updated successfully",
                        "data": {
                            "name": "Updated Name",
                            "email": "updatedemail@example.com",
                            "password": "",  # Password is usually not returned
                        },
                        "softwares": [
                            {
                                "name": "Software A",
                                "status": "Goodware"
                            }
                        ]
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid parameters",
                examples={
                    'application/json': {
                        "error": "Invalid parameters provided."
                    }
                }
            ),
        },
        tags=["Profile"]
    )
    def put(self, request):
        try:
            user = User.objects.filter(pk=request.user.pk)
        except Exception:
            return Response({"error": "Dados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            # Verifica se o username já está em uso por outro usuário
            if username and User.objects.filter(username=username).exists():
                return Response({"error": "Este nome de usuário já está em uso."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Verifica se o email já está em uso por outro usuário
            if email and User.objects.filter(email=email).exists():
                return Response({"error": "Este email já está em uso."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Verifica se a nova senha é igual à senha atual
            if password and check_password(password, user.password):
                return Response({"error": "A nova senha não pode ser igual à senha anterior."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Salva as alterações no perfil
            serializer.save()
            return Response({"message": "Perfil atualizado com sucesso."},
                            status=status.HTTP_200_OK)

        # Se a validação falhar
        return Response({"error": "Dados inválidos."}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    operation_description="Desative ou reative o perfil do usuário",
    request_body=None,  # Não há necessidade de corpo na requisição
    responses={
        200: openapi.Response(
            description="Perfil do usuário atualizado com sucesso",
            examples={
                'application/json': {
                    "message": "Perfil do usuário atualizado com sucesso.",
                    "data": {
                        "name": "Nome Atualizado",
                        "email": "emailatualizado@example.com",
                        "password": "",  # A senha não é retornada por questões de segurança
                    },
                    "softwares": [
                        {
                            "name": "Software A",
                            "status": "Goodware"
                        }
                    ]
                }
            }
        ),
        400: openapi.Response(
            description="Requisição mal formada, parâmetros inválidos",
            examples={
                'application/json': {
                    "error": "Parâmetros inválidos fornecidos."
                }
            }
        ),
    },
    tags=["Profile"]
)
def patch(self, request):
    # Alterna o status de ativação do perfil
    if request.user.is_active:
        request.user.is_active = False
        message = "Perfil desativado com sucesso."
    else:
        request.user.is_active = True
        message = "Perfil reativado com sucesso."

    request.user.save()
    return Response({'message': message}, status=status.HTTP_204_NO_CONTENT)