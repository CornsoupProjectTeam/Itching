# mysql_user_consent.py

from django.db import models

class UserConsent(models.Model):
    user_id = models.OneToOneField('Login', on_delete=models.CASCADE, primary_key=True)
    personal_info_consent = models.BooleanField()
    terms_of_service_consent = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id