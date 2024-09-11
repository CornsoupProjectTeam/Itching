# mysql_postmanagement.py

from django.db import models

class PostManagement(models.Model):
    post_id = models.CharField(max_length=50, primary_key=True)
    user_id = models.ForeignKey('Login', on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    reference_post_id = models.CharField(max_length=50, blank=True, null=True)
    project_title = models.CharField(max_length=255)
    project_or_client_id = models.CharField(max_length=50)  # 프로젝트나 클라이언트 글 ID 속성
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post_id