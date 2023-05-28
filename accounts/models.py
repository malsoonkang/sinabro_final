from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입날짜')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='마지막수정일')


    def __str__(self):
        return self.username


    class Meta:
        db_table = 'user'
        verbose_name = '게시판멤버'
        verbose_name_plural = '게시판멤버'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=255)
    def __str__(self):
        return self.user.username