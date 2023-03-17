from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('add_topic/', views.AddTopicView.as_view(), name='add_topic'),
    path('topic<int:pk>/', views.TopicView.as_view(), name='topic'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('add_avatar/', views.AvatarAddView.as_view(), name='add_avatar'),
    path('grade<int:pk>/', views.GradeRiseCommentView.as_view(), name='plus_comment')
]
