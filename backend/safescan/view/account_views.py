from .views import *

import smtplib
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token

token_generator = PasswordResetTokenGenerator()
User = get_user_model()

from django.contrib.auth import authenticate, login

class SignIn(APIView):
    @swagger_auto_schema(
        operation_description="Login account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username for login'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the user')
            },
            required=['username', 'password'],  # Making fields required
        ),
        responses={
            200: openapi.Response(
                description="User logged in successfully",
                examples={
                    'application/json': {
                        "message": "User logged in successfully.",
                        "token": "your_generated_token_here"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid data",
                examples={
                    'application/json': {
                        "error": "Invalid credentials. Please check the username and password."
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized, invalid credentials",
                examples={
                    'application/json': {
                        "error": "Invalid username or password."
                    }
                }
            ),
            422: openapi.Response(
                description="Validation error",
                examples={
                    'application/json': {
                        "error": "Validation failed. Please check your input data."
                    }
                }
            ),
        },
        tags=["User"]
    )

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

class SignOut(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Log out account",
        request_body=None,  # Nenhum corpo de requisição para o logout
        responses={
            200: openapi.Response(
                description="User logout successfully",
                examples={
                    'application/json': {
                        "message": "User logout successfully."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid data",
                examples={
                    'application/json': {
                        "error": "Invalid request. Please try again."
                    }
                }
            ),
            422: openapi.Response(
                description="Validation error",
                examples={
                    'application/json': {
                        "error": "Validation failed. See field errors for more details."
                    }
                }
            ),
        },
        tags=["User"]
    )
    def delete(self, request):
        # Deleta o token do usuário atual
        try:
            # Busca o token associado ao usuário
            token = Token.objects.get(user=request.user)
            token.delete()  # Deleta o token
            return Response({"message": "Logout bem-sucedido"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"message": "Token não encontrado"}, status=status.HTTP_400_BAD_REQUEST)

class SignUp(APIView):
    # Handling POST request to create a new user with Swagger documentation
    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username for login'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the user')
            },
            required=['username', 'email', 'password'],  # Making fields required
        ),
        responses={
            201: openapi.Response(
                description="User created successfully",
                examples={
                    'application/json': {
                        "message": "User created successfully."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid data",
                examples={
                    'application/json': {
                        "error": "User not created. Check if data is valid."
                    }
                }
            ),
            422: openapi.Response(
                description="Validation error",
                examples={
                    'application/json': {
                        "error": "Validation failed. See field errors for more details."
                    }
                }
            ),
        },
        tags=["User"]
    )
    def post(self, request):
        # Deserialize the request data into the serializer
        serializer = RegisterSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            # Save the new user to the database
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        
        # If validation fails, return error details
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPassword(APIView):
    @swagger_auto_schema(
        operation_description="Forgot password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address of the user'),
            },
            required=['email'],  # Making email field required
        ),
        responses={
            200: openapi.Response(
                description="Password reset email sent successfully",
                examples={
                    'application/json': {
                        "message": "Password reset link has been sent to your email."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid data",
                examples={
                    'application/json': {
                        "error": "Invalid email format. Please check the email address."
                    }
                }
            ),
            404: openapi.Response(
                description="User not found",
                examples={
                    'application/json': {
                        "error": "No user found with this email address."
                    }
                }
            ),
            422: openapi.Response(
                description="Validation error",
                examples={
                    'application/json': {
                        "error": "Validation failed. Please check the email address."
                    }
                }
            ),
        },
        tags=["User"]
    )
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

class ResetPasswordConfirm(APIView):
    @swagger_auto_schema(
        operation_description="Reset password (set a new password)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='New password for the user')
            },
            required=['password'],  # Making password field required
        ),
        responses={
            200: openapi.Response(
                description="Password reset successfully",
                examples={
                    'application/json': {
                        "message": "Your password has been successfully reset."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request, invalid data",
                examples={
                    'application/json': {
                        "error": "Password is required and must meet the security criteria."
                    }
                }
            ),
            404: openapi.Response(
                description="Invalid or expired reset link",
                examples={
                    'application/json': {
                        "error": "The reset link is invalid or has expired."
                    }
                }
            ),
        },
        tags=["User"]
    )
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
