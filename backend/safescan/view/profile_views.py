from .views import *

from ..serializer import ProfileSerializer

class view_profile(APIView):
    permission_classes = [IsAuthenticated]

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

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            # Verifica se o username já está em uso por outro usuário
            if username and User.objects.filter(username=username).exclude(id=request.user.id).exists():
                return Response({"error": "Este nome de usuário já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

            # Verifica se o email já está em uso por outro usuário
            if email and User.objects.filter(email=email).exclude(id=request.user.id).exists():
                return Response({"error": "Este email já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

            # Verifica se a nova senha é igual à senha atual
            if password and check_password(password, request.user.password):
                return Response({"error": "A nova senha não pode ser igual à senha anterior."}, status=status.HTTP_400_BAD_REQUEST)

            # Salva as alterações no perfil
            serializer.save()
            return Response({"message": "Perfil atualizado com sucesso."}, status=status.HTTP_200_OK)

        # Se a validação falhar
        return Response({"error": "Dados inválidos."}, status=status.HTTP_400_BAD_REQUEST)

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
