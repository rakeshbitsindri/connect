from django.db import models

class Device(models.Model):
    ip_address = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.ip_address
