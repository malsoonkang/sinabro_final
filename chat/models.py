from django.db import models
from django.utils.text import slugify
from accounts.models import User
from board.models import Board
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import hashlib


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    users = models.ManyToManyField(User)
    room_board = models.OneToOneField(Board, related_name='chat_room', on_delete=models.CASCADE, null=True, blank=True)
    pw = models.CharField(max_length=4)

    # ...
class one_one_Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    users = models.ManyToManyField(User)




@receiver(post_save, sender=Board)
def create_chat_room(sender, instance, created, **kwargs):
    if created:
        # 4자리 숫자 생성
        random_number = random.randint(1000, 9999)
        # 숫자를 문자열로 변환하여 사용
        slug = str(random_number)
        pw = instance.pw
        print("Creating chat room...")
        print(f"Title: {instance.title}")
        print(f"Slug: {slug}")
        print(f"pw: {instance.pw}")

        # 중복된 slug 값이 있는지 확인
        existing_slugs = Room.objects.filter(slug=slug)
        while existing_slugs.exists():
            # 중복된 slug 값이 있다면, 다시 새로운 무작위 숫자 생성
            random_number = random.randint(1000, 9999)
            slug = str(random_number)
            existing_slugs = Room.objects.filter(slug=slug)

        room = Room.objects.create(name=f"{instance.title} 채팅방", slug=slug, pw=pw, room_board=instance)
        room.users.add(instance.writer)



class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)

@receiver(post_save, sender=Message)
def add_user_to_room(sender, instance, created, **kwargs):
    if created:
        room = instance.room
        user = instance.user
        room.users.add(user)