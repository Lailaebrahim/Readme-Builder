from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class ReadmeWritterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='images/', default='images/default.jpg')
    github_username = models.CharField(max_length=256, null=False)
    github_token = models.CharField(max_length=256, null=True)

    def __str__(self) -> str:
        return self.github_username


@receiver(post_save, sender=User)
def create_user_ReadmeWritterUser(sender, instance, created, **kwargs):
    if created:
        ReadmeWritterUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_ReadmeWritterUser(sender, instance, **kwargs):
    instance.readmewritteruser.save()


class ReadmeFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='ReadmeFiles/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ReadmeFile {self.id} of User {self.user.username}"
