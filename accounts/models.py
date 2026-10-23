from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("PETUGAS", "Petugas / User"),
        ("ADMIN", "Admin"),
        ("SERVER", "Server / Monitoring"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="PETUGAS")
    nama = models.CharField(max_length=150, blank=True)
    jabatan = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    @property
    def is_admin(self):
        return self.role == "ADMIN" or self.user.is_superuser

    @property
    def is_server(self):
        return self.role == "SERVER"

    @property
    def is_petugas(self):
        return self.role == "PETUGAS"
