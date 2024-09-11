# mysql_client_post_list.py

from django.db import models

class ClientPostList(models.Model):
    client_post_id = models.CharField(max_length=50, primary_key=True)
    client_user_id = models.ForeignKey('Login', on_delete=models.CASCADE)
    client_title = models.CharField(max_length=200, blank=True, null=True)
    client_payment_amount = models.IntegerField(blank=True, null=True)
    desired_deadline = models.DateField(blank=True, null=True)
    final_deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_post_id