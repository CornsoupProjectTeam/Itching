# mysql_payment.py

from django.db import models

class Payment(models.Model):
    chat_room_id = models.OneToOneField('ChatRoomMaster', on_delete=models.CASCADE, primary_key=True)
    quotation_id = models.CharField(max_length=50)
    freelancer_user_id = models.ForeignKey('Login', on_delete=models.CASCADE, related_name='freelancer_payments')
    client_user_id = models.ForeignKey('Login', on_delete=models.CASCADE, related_name='client_payments')
    user_name = models.CharField(max_length=100, blank=True, null=True)
    project_title = models.CharField(max_length=200, blank=True, null=True)
    price_unit = models.CharField(max_length=5, blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_st = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chat_room_id