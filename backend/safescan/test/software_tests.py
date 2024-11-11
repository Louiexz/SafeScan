from .tests import *

class SoftwareModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Novouser",
            email="seuemail@gmail.com",
            password=make_password("suasenha")
        )
        self.software = Software.objects.create(
            name="NovoSoftware2",
            status="Malware"
        )

    def test_software_url(self):
        response = self.client.post(reverse("virustotal"), {
            "url": "https://gitlab.com/"
        })
        self.assertEqual(response.status_code, 200)

    def test_list_softwares(self):
        response = self.client.get(reverse("software"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.software.name)

    def test_create_software(self):
        response = self.client.post(reverse("software"), {
            "name": "NovoSoftware1",
            "status": "Malware"
        })
        self.assertEqual(response.status_code, 201)  # Verifica o código de status

        # Verifica se o software foi criado corretamente
        software = Software.objects.get(name="NovoSoftware1")
        self.assertEqual(software.status, "Malware")

    def create_software_logged(self):
        self.client.login(username="Novouser", password="suasenha")
        response = self.client.post(reverse("software"), {
            "name": "NovoSoftware3",
            "status": "Malware"
        })
        software = Software.objects.get(name="NovoSoftware3")
        return software

    def test_delete_software(self):
        self.client.login(username="Novouser", password="suasenha")  # Garantindo que o usuário esteja logado
        response = self.client.delete(reverse("delete-software", kwargs={"id": self.software.id}))

        # Verifica se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verifica se o software foi realmente excluído do banco de dados
        software_exists = Software.objects.filter(id=self.software.id).exists()
        self.assertFalse(software_exists)
