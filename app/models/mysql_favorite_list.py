# mysql_favorite_list.py

from django.db import models

class FavoriteList(models.Model):
    favorite_list_id = models.CharField(max_length=50, primary_key=True)
    user_id = models.ForeignKey('Login', on_delete=models.CASCADE, related_name='favorites')
    author_id = models.ForeignKey('Login', on_delete=models.CASCADE, related_name='favorite_authors')
    favorite_post_id = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.favorite_list_id