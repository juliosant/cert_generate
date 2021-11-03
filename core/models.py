from django.db import models

# Create your models here.

class CertificateRevocation(models.Model):
    serial_number = models.CharField(max_length=1000)

