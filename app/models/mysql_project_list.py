# mysql_project_list.py

from django.db import models

class ProjectList(models.Model):
    project_id = models.CharField(max_length=50, primary_key=True)
    public_profile_id = models.ForeignKey('PublicProfile', on_delete=models.CASCADE)
    freelancer_user_id = models.ForeignKey('Login', on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    field = models.CharField(max_length=100, blank=True, null=True)
    project_payment_amount = models.IntegerField()
    main_image_path = models.CharField(max_length=255, blank=True, null=True)
    service_options = models.TextField(blank=True, null=True)
    avg_response_time = models.IntegerField(blank=True, null=True)
    freelancer_badge = models.CharField(max_length=10, blank=True, null=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_id