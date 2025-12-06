from django.urls import path
from . import views
from .views import available_matches_view
from .views import all_matches_view, update_status_result


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_view, name='login_view'),
    path("register/", views.register_view, name="register"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile_view'),
    path('delete-photo/<int:photo_id>/', views.delete_photo_view, name='delete_photo'),
    path("about-feedback/", views.about_feedback, name="about_feedback"),
    path('save-feedback/', views.save_feedback, name='save_feedback'),
    path('schedule/', views.schedule_match_view, name='schedule_match'),
    path('available-matches/', available_matches_view, name='available_matches'),
    path('all-matches/', all_matches_view, name='all_matches'),
    path('all-matches/<int:match_id>/<str:result>/', update_status_result, name='update_match_result'),
    path("join-group/<int:match_id>/", views.join_group, name="join_group"),
    path("search/", views.search_users_view, name="search_users"),
    path('profile/<int:user_id>/', views.view_other_profile, name='view_profile'),
    path("update-status-result/<int:match_id>/", views.update_status_result, name="update_status_result"),
    path('notes/', views.notes_view, name='notes'),
    path('notes/delete/<int:pk>/', views.delete_note, name='delete_note'),


]
