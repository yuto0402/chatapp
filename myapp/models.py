from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your mode
class CustomUser(AbstractUser):
    image = models.ImageField('Img', upload_to='img/', null=True, blank=True)
    following = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
        )

    def __str__(self):
        return str(self.username)
    
class TalkRoom(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender', null=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver', null=True)
    talkDate = models.DateTimeField(verbose_name='会話日時', auto_now=True)
    message = models.TextField(verbose_name='メッセージ', blank=True, null=True)
