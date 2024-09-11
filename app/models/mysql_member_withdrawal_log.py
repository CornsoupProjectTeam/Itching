# mysql_member_withdrawal_log.py

from django.db import models

class MemberWithdrawalLog(models.Model):
    user_id = models.OneToOneField('Login', on_delete=models.CASCADE, primary_key=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    withdrawal_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id