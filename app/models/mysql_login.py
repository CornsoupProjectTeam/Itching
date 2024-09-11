# mysql_login.py

from django.db import models

class Login(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    provider_id = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id