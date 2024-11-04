from django.urls import reverse
from .views import *

from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

token_generator = PasswordResetTokenGenerator()

@api_view(["GET", "POST"])
def sign_in(request):
    if request.method == "GET":
        return Response({"message": "Enter Username and password to continue."}, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"error": "Username e password são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(username=username)
        user.refresh_from_db()
        if check_password(password, user.password):
            login(request, user)
            return Response({"message": "Login bem-sucedido"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({'error': 'Invalid method.'},
                      status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET", "POST"])
def sign_up(request):
    if request.method == "GET":
        return Response({"message": "Enter Username, email and password to register."}, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "User not created."}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Invalid method.'},
                      status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET", "POST"])
def forgot_password(request):
    if request.method == "GET":
        return Response({"message": "Enter email to forgot password."}, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
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
            
            reset_link = request.build_absolute_uri(reverse('reset-password', kwargs={'uidb64': uid, 'token': token}))
            
            send_mail(
                "Recuperação de senha",
                f"Use o link abaixo para redefinir sua senha:\n{reset_link}",
                f"fluizlucas@gmail.com",  # Substitua pelo seu endereço de e-mail de envio
                [user.email],
            )
            return Response({'message': 'Email para recuperação de senha enviado.'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': 'Email para recuperação de senha não foi enviado.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Invalid method.'},
                      status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET", "PATCH"])
def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64)).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if request.method == "GET":
        return Response({'message': 'Digite a nova senha.'}, status=status.HTTP_200_OK)
    
    elif request.method == "PATCH":
        new_password = request.data.get('password')
        if not new_password:
            return Response({"error": "Nova password é obrigatória."}, status=status.HTTP_400_BAD_REQUEST)
        
        if (check_password(new_password, user.password)):
            return Response({"error": "Senha igual a anterior."}, status=status.HTTP_400_BAD_REQUEST)

        if user is not None and token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Senha alterada com sucesso.'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Token inválido ou expirado.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Invalid method.'},
                      status=status.HTTP_405_METHOD_NOT_ALLOWED)
