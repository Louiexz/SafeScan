from .models import *
class Software(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    label = models.CharField(max_length=20, choices=[
        ("Malware", "Malware"),
        ("Goodware", "Goodware")
    ])  # Mapeado diretamente como Label
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="softwares", null=True)

    # Features com nomes completos
    localizacao_rede = models.BooleanField(default=False)
    bluetooth_funcionalidades = models.BooleanField(default=False)
    arquivos_confOS = models.BooleanField(default=False)
    sms = models.BooleanField(default=False)
    midia_audio = models.BooleanField(default=False)
    camera = models.BooleanField(default=False)
    rede_operadora = models.BooleanField(default=False)
    sim_pais = models.BooleanField(default=False)
    biblioteca_class = models.BooleanField(default=False)
    pacotes = models.BooleanField(default=False)

    def __str__(self):
        return f"Software '{self.name}', Created at: {self.created_at}, Last update: {self.updated_at} Label: {self.label}."