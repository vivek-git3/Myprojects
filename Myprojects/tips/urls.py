from django.urls import path
from . import views
from .views import MyTipsView, EditTipView, DeleteTipView, TipDetailView,HomeView, SearchTipsView,remove_like,user_login,user_logout,password_reset_request
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('add_tip/', views.add_tip, name='add_tip'),
    path('my_tips/', views.my_tips, name='my_tips'),
    path('liked_tips/', views.liked_tips, name='liked_tips'),
    path('logout/', views.user_logout, name='logout'),
    path('search_tips/', views.search_tips, name='search_tips'),
    path('like_tip/<int:tip_id>/', views.like_tip, name='like_tip'),
    path('share_tip/<int:tip_id>/', views.share_tip, name='share_tip'),
    path('search/', views.search_tips, name='search_tips'),  
    path('my_tips/', MyTipsView.as_view(), name='my_tips'),
    path('edit_tip/<int:tip_id>/', EditTipView.as_view(), name='edit_tip'),
    path('delete_tip/<int:tip_id>/', DeleteTipView.as_view(), name='delete_tip'),
    path('tip/<int:tip_id>/', TipDetailView.as_view(), name='tip_detail'),
    path('', HomeView.as_view(), name='home'),
    path('remove_like/<int:tip_id>/', remove_like, name='remove_like'),
    path('accounts/login/', user_login, name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    path('password_reset/', password_reset_request, name='password_reset'),

]
