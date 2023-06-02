from django.urls import path

from . import views

urlpatterns = [
    path("create_chat_room/<int:board_id>/", views.create_chat_room, name='create_chat_room'),
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),
]