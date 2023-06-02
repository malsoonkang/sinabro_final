from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, reverse, redirect
from .models import Room, Message
from django.shortcuts import get_object_or_404
from board.models import Board
from .models import one_one_Room
from accounts.models import User
import random


@login_required
def rooms(request):
    user = request.user
    rooms = Room.objects.filter(users=user)

    return render(request, 'chat/rooms.html', {'rooms': rooms})


@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)

    if request.method == 'POST':
        room_pw = request.POST.get('pw')

        if room_pw == room.pw or room.pw is None:
            messages = Message.objects.filter(room=room).order_by('-id')[:50][::-1]
            return render(request, 'chat/room.html', {'room': room, 'messages': messages})
        else:
            board = get_object_or_404(Board, chat_room=room)
            return render(request, 'board/board_detail.html', {'board': board, 'room_error': '비밀번호가 올바르지 않습니다.'})
    else:
        messages = Message.objects.filter(room=room).order_by('-id')[:50][::-1]
        return render(request, 'chat/room.html', {'room': room, 'messages': messages})



@login_required
def create_chat_room(request, board_id):
    user1 = request.user
    board = get_object_or_404(Board, id=board_id)
    user2 = board.writer  # 게시자(유저2)
    random_number = random.randint(1000, 9999)
    slug = str(random_number)

    existing_slugs = Room.objects.filter(slug=slug)
    while existing_slugs.exists():
        # 중복된 slug 값이 있다면, 다시 새로운 무작위 숫자 생성
        random_number = random.randint(1000, 9999)
        slug = str(random_number)
        existing_slugs = Room.objects.filter(slug=slug)

    room = Room.objects.filter(users=user1).filter(users=user2).filter(room_board__isnull=True).first()
    if room:
        # 이미 유저1과 유저2를 가진 room_board가 null인 채팅방이 존재하는 경우, 해당 채팅방으로 이동
        messages = Message.objects.filter(room=room).order_by('-id')[:50][::-1]
        return render(request, 'chat/room.html', {'room': room, 'messages': messages})

    room = Room.objects.create(name=f"{user1.username} 님과 {user2.username}'님의 채팅방", slug=slug)
    room.users.add(user1, user2)
    messages = Message.objects.filter(room=room).order_by('-id')[:50][::-1]
    return render(request, 'chat/room.html', {'room': room, 'messages': messages})
