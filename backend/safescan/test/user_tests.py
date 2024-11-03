from .tests import *

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
