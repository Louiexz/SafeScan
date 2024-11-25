from .views import *

import smtplib
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout

token_generator = PasswordResetTokenGenerator()
User = get_user_model()

from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
class sign_in(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username e password são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            # Generate or retrieve the token for the user
            token, created = Token.objects.get_or_create(user=user)

            # Log the user in (this creates a session if using SessionAuthentication)
            login(request, user)

            # Return success response with token and message
            return Response({
                "message": "Login bem-sucedido",
                "token": token.key  # Return only the token key
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciais inválidas ou usuário inativo"}, status=status.HTTP_401_UNAUTHORIZED)
    
class sign_out(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Deleta o token do usuário atual
        try:
            # Busca o token associado ao usuário
            token = Token.objects.get(user=request.user)
            token.delete()  # Deleta o token
            return Response({"message": "Logout bem-sucedido"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"message": "Token não encontrado"}, status=status.HTTP_400_BAD_REQUEST)

class sign_up(APIView):
    def get(self, request):
        return Response({"message": "Enter Username, email and password to register."}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "User not created."}, status=status.HTTP_400_BAD_REQUEST)

class forgot_password(APIView):
    def get(self, request):
        return Response({"message": "Enter email to forgot password."}, status=status.HTTP_200_OK)
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado com esse email."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            reset_link = f"http://localhost:5173/confirm/{uid}/{token}"
     
            send_mail(
                "Recuperação de senha",
                f"Use o link abaixo para redefinir sua senha:\n{reset_link}",
                "fluizlucas@gmail.com",  # Substitua pelo seu endereço de e-mail de envio
                [user.email],
            )
            return Response({'message': 'Email para recuperação de senha enviado.'}, status=status.HTTP_200_OK)
        
        except smtplib.SMTPException as e:
            return Response({'error': f'Erro ao enviar o e-mail de recuperação de senha: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class reset_password_confirm(APIView):
    def patch(self, request, uidb64, token):
        try:
            # Decodifica o uid e tenta buscar o usuário
            uid = force_bytes(urlsafe_base64_decode(uidb64)).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Token inválido ou expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('password')
        if not new_password:
            return Response({"error": "Nova password é obrigatória."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se a senha nova é igual à antiga
        if check_password(new_password, user.password):
            return Response({"error": "Senha igual a anterior."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o token é válido
        if token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Senha alterada com sucesso.'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Token inválido ou expirado.'}, status=status.HTTP_400_BAD_REQUEST)
