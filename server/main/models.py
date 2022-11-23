from django.db import models

# Create your models here.
class GithubUser(models.Model):
    name = models.CharField(max_length=254)
    github_handle = models.CharField(max_length=254)
    blurb = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=254, null=True, blank=True)
    github_profile_link = models.URLField()
    twitter_handle = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
