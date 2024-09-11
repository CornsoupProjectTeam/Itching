# mysql_chat_room_master.py

from django.db import models

class ChatRoomMaster(models.Model):
    chat_room_id = models.CharField(max_length=50, primary_key=True)
    quotation_id = models.CharField(max_leㅁngth=50, blank=True, null=True)
    freelancer_user_id = models.ForeignKey('Login', on_delete=models.CASCADE, related_name='freelancer_chatrooms', blank=True, null=True)
    client_user_id = models.ForeignKey('Login', on_delete=models.CASCADE, related_name='client_chatrooms', blank=True, null=True)
    start_post_id = models.CharField(max_length=50, blank=True, null=True)
    freelancer_trade_status = models.IntegerField()
    client_trade_status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chat_room_id