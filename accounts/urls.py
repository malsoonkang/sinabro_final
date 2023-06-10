from django.urls import path
from django.contrib.auth import views as auth_views
import accounts.views as user_views
from accounts import views

urlpatterns = [
    path("register/", user_views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),
    path('mypage/<str:username>/', views.mypage, name='user_mypage'),
    #path('mypage/', views.mypage, name='mypage'),
    path('delete_profile_image/', views.delete_profile_image, name='delete_profile_image'),
]
