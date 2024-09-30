from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.show, name='show'),

    path('footer/', views.footer,name='footer'),
    path('generate/', views.generate_view, name='generate_lyrics'),
    path('delete_lyric/<int:lyric_id>/', views.delete_lyric, name='delete_lyric'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('about/', views.about_view, name='about_view'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('music_list', views.music_list, name='music_list'),
    path('add/', views.add_music, name='add_music'),
    path('delete/<int:pk>/', views.delete_music, name='delete_music'),
    path('edit/<int:music_id>/', views.edit_music, name='edit_music'),

    path('fav', views.favorites_page, name='favorites_page'),
    path('add_to_favorites/<int:music_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:music_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('terminate_user/<int:user_id>/', views.terminate_user, name='terminate_user'),
    path('user_management/', views.user_management, name='user_management'),

    path('daily_report/', views.daily_report, name='daily_report'),

]
