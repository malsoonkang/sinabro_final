from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from accounts.forms import UserRegisterForm, UserProfileForm
from .models import Profile
from board.models import Board


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(
                request, f" 회원가입에 성공하셨습니다 {username} 님"
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})

@login_required
def mypage(request):
    user = request.user
    if request.method == 'POST':
        emoji = request.POST.get('emoji', '')  # 폼에서 이모지 값을 가져옴
        user_profile = Profile.objects.get(user=user)
        user_profile.emoji = emoji
        user_profile.save()
    if request.user.is_authenticated:
        liked_posts = Board.objects.filter(likes=request.user)
        return render(request, 'accounts/mypage_main.html', {'liked_posts': liked_posts})
    else:

        return render(request, 'accounts/mypage_main.html', {'user': user})

def save_emoji(request):
    if request.method == 'POST':
        emoji = request.POST.get('emoji', '')
        # 이모지 값을 처리하고 저장하는 로직을 추가하세요

        # 성공적으로 저장되었다고 가정하고, 이미지 URL을 반환합니다.
        image_url = "https://example.com/profile-image.png"  # 저장된 이미지 URL

        return JsonResponse({'success': True, 'image_url': image_url})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})



