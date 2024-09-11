# mysql_email_notification.py

from django.db import models

class EmailNotification(models.Model):
    sequence = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('Login', on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    message_type = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.message_type}"