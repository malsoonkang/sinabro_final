from django.urls import path
from hitcount.views import HitCountDetailView
from . import views
from .models import Board


urlpatterns = [
    path('list/', views.board_list),
    path('write/', views.board_write),
    path('detail/<int:pk>/', HitCountDetailView.as_view(model=Board, count_hit=True), name='board_detail'),
    #path('detail/<int:pk>/', views.board_detail),
    path('modify/<int:pk>/', views.board_modify, name='board_modify'),
    path('delete/<int:pk>/', views.board_delete, name='board_delete'),
    path('list/search/', views.search_view, name='search'),
    path('post/', views.board_posts, name='board_post'),
    path('like/<int:board_id>/', views.like_post, name="like_post"),
]
