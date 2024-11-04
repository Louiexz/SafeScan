from .models import *

class Software(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ("Malware", "Malware"),
        ("Goodware", "Goodware")
    ])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="softwares", null=True)
    
    def __str__(self):
        return f"Software '{self.name}', Created at: {self.created_at}, Last update: {self.updated_at} Status: {self.status}."
