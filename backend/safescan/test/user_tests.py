from .tests import *

import json

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
token_generator = PasswordResetTokenGenerator()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Novouser2",
            email="seuemail@gmail.com",
            password=make_password("suasenha")
        )

    def login(self):
        response = self.client.post(reverse("sign-in"), {
            "username":"Novouser2",
            "password":"suasenha"
        })
        assert 'token' in response.data, f"Token não encontrado na resposta: {response.data}"  # Melhor mensagem de erro

        token = response.data["token"]

        # Criando o cabeçalho de autenticação com o token
        headers = {"Authorization": f"Token {token}"}
        return response, headers

    def test_login_users(self):
        response, headers = self.login()
        self.assertEqual(response.status_code, 200)
    
    def test_logout_users(self):
        login, headers = self.login()

        # Send the DELETE request with the token in the headers
        response = self.client.delete(reverse("sign-out"), HTTP_AUTHORIZATION=headers["Authorization"])

        self.assertEqual(response.status_code, 200)
    
    def test_create_software_logged(self):
        login, headers = self.login()

        response = self.client.post(reverse("software_form_auth"), {
            "name": "NovoSoftware2",
            'localizacao_rede': 1,
            'bluetooth_funcionalidades': 1,
            'arquivos_confOS': 1,
            'sms': 1,
            'midia_audio': 1,
            'camera': 1,
            'rede_operadora': 1,
            'sim_pais': 1,
            'biblioteca_class': 1,
            'pacotes': 1,
        }, HTTP_AUTHORIZATION=headers["Authorization"])

        self.assertEqual(response.status_code, 201)
        software = Software.objects.get(name="NovoSoftware2")
        self.assertEqual(software.label, "Malware")

    def test_update_user(self):
        login, headers = self.login()

        response = self.client.put(reverse("profile-update"), {
        json.dumps({
            "username": "UserAtualizado",
            "email": "novoemail@gmail.com",
            "password": "suasenha2",
        }),
        }, HTTP_AUTHORIZATION=headers["Authorization"], content_type="application/json")

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.username, "UserAtualizado")
        self.assertEqual(self.user.email, "novoemail@gmail.com")
        self.assertEqual(self.user.password, "suasenha2")

    def test_create_user(self):
        response = self.client.post(reverse("sign-up"), {
            "username": "Novouser1",
            "email": "seuemail2@gmail.com",
            "password": "suasenha5"
        })

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="Novouser1")
        self.assertEqual(user.email, "seuemail2@gmail.com")
        self.assertTrue(check_password("suasenha5", user.password))
    
    def test_list_users(self):
        login, headers = self.login()

        response = self.client.get(reverse("profile"), HTTP_AUTHORIZATION=headers["Authorization"])

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    """def test_delete_user(self):
        self.client.login(username="Novouser2", password="suasenha")
        response = self.client.patch(reverse("profile"))
        self.assertEqual(response.status_code, 204)"""

    def test_reset_password(self):
        response = self.client.post(reverse("forgot-password"), {
            "email":"novoemail@gmail.com",
        }, content_type="application/json")

        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = token_generator.make_token(self.user)

        response = self.client.patch(reverse("reset-password", kwargs={'uidb64': uid, 'token': token}), {
            "password":"suasenha1",
        }, content_type="application/json")

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 202)
        self.assertTrue(check_password("suasenha1", self.user.password))