from django.urls import path
from hitcount.views import HitCountDetailView
from . import views
from django.conf.urls.static import static
from .models import Board


urlpatterns = [
    path('list/', views.board_list),
    path('write/', views.board_write),
    path('detail/<int:pk>/', views.board_detail, name='board_detail'),
    #path('detail/<int:pk>/', HitCountDetailView.as_view(model=Board, count_hit=True), name='board_detail'),
    path('modify/<int:pk>/', views.board_modify, name='board_modify'),
    path('delete/<int:pk>/', views.board_delete, name='board_delete'),
    path('list/search/', views.search_view, name='search'),
    path('post/', views.board_posts, name='board_post'),
    path('like/<int:board_id>/', views.like_post, name="like_post"),
    path('board/<int:pk>/comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('portfolio_write/', views.create_portfolio_post, name='create_portfolio_post'),
    path('portfolio_list/', views.portfolio_list, name='portfolio_list'),
    path('portfolio_list/<int:portfolio_id>', views.portfolio_detail, name='portfolio_detail'),
    path('portfolio_update/<int:portfolio_id>/', views.update_portfolio_post, name='update_portfolio_post'),
    path('portfolio_delete/<int:portfolio_id>/', views.delete_portfolio_post, name='delete_portfolio_post'),
]
