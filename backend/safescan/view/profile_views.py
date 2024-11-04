from .views import *

from ..serializer import ProfileSerializer, SoftwareSerializer

@api_view(["GET", "PUT", "DELETE"])
def view_profile(request):
    if not request.user.is_authenticated:
        return Response({"error": "Usuário deslogado."}, status=status.HTTP_404_NOT_FOUND)
    else:
        profileData = User.objects.get(username=request.user.username)

    if request.method == "GET":
        profileData.password = "*****"
        serializer = ProfileSerializer(profileData)
        try:
            # Busca todos os softwares associados ao usuário logado
            softwareData = Software.objects.filter(user_id=request.user.id)
            
            # Serializa a lista de softwares do usuário
            softwareSerialize = SoftwareSerializer(softwareData, many=True)

            return Response({
                "message": "User profile data.",
                "data": serializer.data,
                "softwares": softwareSerialize.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "message": "User profile data.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = ProfileSerializer(profileData, data=request.data)

        if serializer.is_valid():
            try:
                username = serializer.validated_data.get("username")
                password = serializer.validated_data.get("password")
                email = serializer.validated_data.get("email")

                # Verifica se o username já está em uso por outro usuário
                if User.objects.filter(username=username).exists():
                    return Response({"error": "Este usuário já existe."}, status=status.HTTP_401_UNAUTHORIZED)

                # Verifica se o email já está em uso por outro usuário
                if User.objects.filter(email=email).exists():
                    return Response({"error": "Este email já existe."}, status=status.HTTP_401_UNAUTHORIZED)
                
                # Verifica se a nova senha é igual à senha atual
                if check_password(password, request.user.password):
                    return Response({"error": "A nova senha não pode ser igual à senha anterior."}, status=status.HTTP_401_UNAUTHORIZED)
                serializer.validated_data["password"] = make_password(password)
                serializer.save()
                return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
            
            except Exception as e:
                # Captura qualquer outro erro inesperado
                return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == "DELETE":
        profileData.delete()
        return Response({'message': 'Profile deleted successfully.'},
                      status=status.HTTP_204_NO_CONTENT)

    return Response({'error': 'Invalid method.'},
                      status=status.HTTP_405_METHOD_NOT_ALLOWED)
