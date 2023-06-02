from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from accounts.forms import UserRegisterForm, UserProfileForm
from accounts.models import User, Profile
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
    profile, created = Profile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile.profile_image = form.cleaned_data['profile_image']
            form.save()
            return redirect('mypage')
    else:
        form = UserProfileForm(instance=profile)

    if request.user.is_authenticated:
        liked_posts = Board.objects.filter(likes=request.user)
        return render(request, 'accounts/mypage_main.html', {'liked_posts': liked_posts, 'user': user, 'form': form})
    else:
        return render(request, 'accounts/mypage_main.html', {'user': user, 'form': form})

@login_required
def delete_profile_image(request):
    user = request.user
    profile = user.profile
    if profile.profile_image:
        profile.profile_image.delete(save=False)
        profile.profile_image = None
        profile.save()
    return JsonResponse({'message': '프로필 이미지가 기본이미지로 변경되었습니다.'})



