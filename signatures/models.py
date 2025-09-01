import uuid
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    public_key = models.TextField()
    private_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Signature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    signature = models.TextField()
    timestamp = models.BigIntegerField()

    def __str__(self):
        return f"Assinatura de {self.signer.username} em {self.timestamp}"

class VerificationLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    signature_id = models.UUIDField(null=True)
    is_valid = models.BooleanField()
    reason = models.TextField()
    timestamp = models.BigIntegerField()
    
    def __str__(self):
        return f"Verificação de {self.signature_id}: {self.is_valid}"