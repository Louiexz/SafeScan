from .tests import *
class SoftwareModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Novouser",
            email="seuemail@gmail.com",
            password=make_password("suasenha")
        )
        self.software = Software.objects.create(
            name="NovoSoftware",
            localizacao_rede=1,
            bluetooth_funcionalidades=1,
            arquivos_confOS=1,
            sms=1,
            midia_audio=1,
            camera=1,
            rede_operadora=1,
            sim_pais=1,
            biblioteca_class=1,
            pacotes=1,
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
        response = self.client.post(reverse("software_form_unauth"), {
            "name": "NovoSoftware1",
            'localizacao_rede': 1,  # Acesso à localização pode ser legítimo, mas precisa ser monitorado
            'bluetooth_funcionalidades': 0,  # O Bluetooth não deve ser ativado sem necessidade legítima
            'arquivos_confOS': 0,  # Não deve haver acesso ou modificação de arquivos críticos do sistema
            'sms': 1,  # O envio de SMS pode ser legítimo, mas precisa ser monitorado para abuso
            'midia_audio': 0,  # O acesso à mídia de áudio sem necessidade é um comportamento suspeito
            'camera': 0,  # O acesso à câmera sem justificativa pode indicar espionagem
            'rede_operadora': 0,  # Não deve haver acesso à rede da operadora sem justificativa
            'sim_pais': 1,  # Pode ser necessário para funcionalidades legítimas, mas precisa ser monitorado
            'biblioteca_class': 0,  # Carregar bibliotecas externas sem necessidade pode indicar código malicioso
            'pacotes': 1  # Uso de pacotes de dados pode ser legítimo, mas deve ser monitorado para tráfego suspeito
        })
        self.assertEqual(response.status_code, 201)  # Verifica o código de status

        # Verifica se o software foi criado corretamente
        software = Software.objects.get(name="NovoSoftware1")
        self.assertEqual(software.label, "Goodware")

    def test_delete_software(self):
        self.client.login(username="Novouser", password="suasenha")  # Garantindo que o usuário esteja logado
        response = self.client.delete(reverse("delete-software", kwargs={"id": self.software.id}))

        # Verifica se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verifica se o software foi realmente excluído do banco de dados
        software_exists = Software.objects.filter(id=self.software.id).exists()
        self.assertFalse(software_exists)
