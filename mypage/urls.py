from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    # 기타 URL 매핑
    path('upload_background/', views.upload_background, name='upload_background'),
]
