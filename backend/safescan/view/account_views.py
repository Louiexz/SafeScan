from .views import *

from django.contrib.auth import login, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()
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
    
    return Response({'message': 'Método inválido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET", "POST"])
def sign_up(request):
    if request.method == "GET":
        return Response({"message": "Enter Username, email and password to register."}, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'message': 'Invalid method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET", "POST"])
def retrieve_password(request):
    if request.method == "GET":
        return Response({"message": "Enter email to retrieve password."}, status=status.HTTP_200_OK)
    
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
            
            reset_link = f"http://safeclean.vercel.app/reset-password/{uid}/{token}/"
            
            send_mail(
                "Recuperação de senha",
                f"Use o link abaixo para redefinir sua senha:\n{reset_link}",
                f"fluizlucas@safeclean.com",  # Substitua pelo seu endereço de e-mail de envio
                [user.email],
            )
            return Response({'message': 'Email para recuperação de senha enviado.'}, status=status.HTTP_200_OK)
        
        except Exception:
            return Response({'message': 'Email para recuperação de senha não foi enviado.'}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["POST"])
def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64)).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        new_password = request.data.get('password')
        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Senha alterada com sucesso.'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': 'Nova senha é obrigatória.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Token inválido ou expirado.'}, status=status.HTTP_400_BAD_REQUEST)
