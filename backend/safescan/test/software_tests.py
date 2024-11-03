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
        response = self.client.post(reverse("software"), {
            "url":"https://gitlab.com/"
        })
        self.assertEqual(response.status_code, 200)

    def test_list_softwares(self):
        response = self.client.get(reverse("software"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.software.name)
    
    def test_create_software(self):
        response = self.client.post(reverse("software"), {
            "name":"NovoSoftware1",
            "status":"Malware"
        })
        software = Software.objects.get(name=self.software.name)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(software.status, "Malware")
    
    def create_software_logged(self):
        self.client.login(username="Novouser", password="suasenha")
        response = self.client.post(reverse("software"), {
            "name":"NovoSoftware3",
            "status":"Malware"
        })
        software = Software.objects.get(name="NovoSoftware3")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(software.status, "Malware")
        return software

    def test_update_software(self):
        self.client.login(username="Novouser", password="suasenha")
        software_logged = self.create_software_logged()
        response = self.client.put(reverse("software"), {
            "id": software_logged.id,
            "name":"NovoSoftware1",
            "status":"Goodware"
        }, content_type="application/json")
        software_logged.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(software_logged.status, "Goodware")
