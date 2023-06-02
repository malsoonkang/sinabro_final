from accounts.models import User, Profile
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserRegisterForm(UserCreationForm):

    class Meta:
        model= User
        fields = ['username', 'password1', 'password2',]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # 모델 클래스를 지정해야 합니다
        fields = ['profile_image']  # 필드 목록을 지정해주세요




