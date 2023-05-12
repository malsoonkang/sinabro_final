from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.board_list),
    path('write/', views.board_write),
    path('detail/<int:pk>/', views.board_detail),
    path('modify/<int:pk>/', views.board_modify, name='board_modify'),
    path('delete/<int:pk>/', views.board_delete, name='board_delete'),
    path('list/search/', views.search_view, name='search'),
]
