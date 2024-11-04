from .tests import *

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

    def test_login_users(self):
        response = self.client.post(reverse("sign-in"), {
            "username":"Novouser2",
            "password":"suasenha"
        })
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.post(reverse("sign-up"), {
            "username": "Novouser1",
            "email": "seuemail2@gmail.com",
            "password": "suasenha"
        })
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="Novouser1")
        self.assertEqual(user.email, "seuemail2@gmail.com")
        self.assertTrue(check_password("suasenha", user.password))
    
    def test_list_users(self):
        self.client.login(username="Novouser2", password="suasenha")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_update_user(self):
        self.client.login(username="Novouser2", password="suasenha")
        response = self.client.put(reverse("profile"), {
            "username":"UserAtualizado",
            "email":"novoemail@gmail.com",
            "password":"suasenha1"
        }, content_type="application/json")
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.username, "UserAtualizado")
        self.assertEqual(self.user.email, "novoemail@gmail.com")
        self.assertTrue(check_password("suasenha1", self.user.password))

    def test_delete_user(self):
        self.client.login(username="Novouser2", password="suasenha")
        response = self.client.delete(reverse("profile"))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 0)

    def test_reset_password(self):
        self.client.login(username="Novouser2", password="suasenha")
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