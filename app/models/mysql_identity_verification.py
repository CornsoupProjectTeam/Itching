# mysql_identity_verification.py

from django.db import models

class IdentityVerification(models.Model):
    user_id = models.OneToOneField('Login', on_delete=models.CASCADE, primary_key=True)
    verification_status = models.BooleanField()
    phone_number = models.CharField(max_length=20)
    verification_code = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id