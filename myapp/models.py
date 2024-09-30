from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your mode
class CustomUser(AbstractUser):
    email = models.EmailField('Email address')
    image = models.ImageField('Img', upload_to='img/', null=True, blank=True)

    def __str__(self):
        return str(self.username)

class Friend(models.Model):
    class Meta:
        verbose_name = "Friend"
        verbose_name_plural = "Friend"

    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE, related_name='User', null=True)
    friend = models.ForeignKey(CustomUser, verbose_name='友達', on_delete=models.CASCADE, related_name='Friend', null=True)
    
class TalkRoom(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender', null=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver', null=True)
    talkDate = models.DateTimeField(verbose_name='会話日時', auto_now=True)
    message = models.TextField(verbose_name='メッセージ', blank=True, null=True)
