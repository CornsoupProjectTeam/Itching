# mysql_public_profile.py

from django.db import models

class PublicProfile(models.Model):
    public_profile_id = models.CharField(max_length=30, primary_key=True)
    freelancer_user_id = models.ForeignKey('Login', on_delete=models.CASCADE)
    profile_image_path = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=20)
    matching_count = models.IntegerField(default=0)
    service_option = models.TextField(blank=True, null=True)
    avg_response_time = models.IntegerField(blank=True, null=True)
    price_unit = models.CharField(max_length=5, blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    freelancer_badge = models.CharField(max_length=10, blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.public_profile_id