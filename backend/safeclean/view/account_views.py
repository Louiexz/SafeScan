from .views import *

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login
from ..serializer import UserSerializer

@api_view(["GET", "POST"])
def sign_in(request):
    if request.method == "GET":
        return Response({"message":"Enter Username and password to continue."}, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        # Verifique se os dados enviados são válidos
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Autentique o usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({"message": "Login bem-sucedido"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'message': 'Invalid method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
@api_view(["GET", "POST"])
def sign_up(request):
    if request.method == "GET":
        return Response({"message":"Enter Username, email and password to register."}, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({"message":"User created sucessfully."}, status=status.HTTP_201_CREATED)
        return Response({"message":"User not created sucessfully."}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'message': 'Invalid method.'},
                      status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET", "POST"])
def retrieve_password(request):
    token = token_generator.make_token(request.user)

    if request.method == "GET":
        token_generator = PasswordResetTokenGenerator()
        uid = urlsafe_base64_encode(force_bytes(request.user.pk))

        # Construir o link de recuperação
        reset_link = f"http://safeclean.vercel.app/reset-password/{uid}/{token}/"

        # Enviar o e-mail
        send_mail(
            "Recuperação de senha",
            f"Use o link abaixo para redefinir sua senha:\n{reset_link}",
            "noreply@safeclean.com",
            [request.user.email],
        )
        return Response({'message': 'Email para recuperação de senha enviado.'},
                      status=status.HTTP_200_OK)
    
    if request.method == "POST":
        profileData = User.objects.filter(user=request.user)
        serializer = UserSerializer(profileData, data=request.data)

        if request.data.get('token') == token:
            serializer.password = request.data.get('password')
            serializer.save()

            return Response({'message': 'Token agree. Altered password.'},
                      status=status.HTTP_202_ACCEPTED)