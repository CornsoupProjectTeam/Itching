# mysql_faq.py

from django.db import models

class FAQ(models.Model):
    faq_id = models.CharField(max_length=20, primary_key=True)
    category_faq = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.faq_id