from django.shortcuts import render, redirect
from .forms import BackgroundImageForm
from django.contrib.auth.decorators import login_required

@login_required
def upload_background(request):
    if request.method == 'POST':
        form = BackgroundImageForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('mypage:upload_background')  # 마이페이지로 리디렉션
    else:
        form = BackgroundImageForm(instance=request.user.userprofile)
    return render(request, 'mypage/mypage_main.html', {'form': form})



