from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status/', views.CreateStatusMessageView.as_view(), name='create_status'),
    path('status/create_status/', views.CreateStatusMessageView.as_view(), name='status_create_status'),  # NEW
    path('profile/<int:pk>/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='profile_update'),  # NEW
    path('status/<int:pk>/delete/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/<int:pk>/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='add_friend'),
    path('profile/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='profile_add_friend'),  # NEW
    path('profile/<int:pk>/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='profile_friend_suggestions'),  # NEW
    path('profile/<int:pk>/news_feed/', views.ShowNewsFeedView.as_view(), name='news_feed'),
    path('profile/news_feed/', views.ShowNewsFeedView.as_view(), name='profile_news_feed'),  # NEW
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'),
]
