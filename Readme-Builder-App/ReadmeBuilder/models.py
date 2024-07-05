from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, null=False)
    email = models.CharField(unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    github_username = models.CharField(unique=True, null=False)
    github_token = models.CharField()


class ReadmeFile(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=False)
