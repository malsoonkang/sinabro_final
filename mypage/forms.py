from django import forms
from .models import UserProfile

class BackgroundImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['background_image']
