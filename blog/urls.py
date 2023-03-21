from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', login_required(views.LogoutView.as_view()), name='logout'),
    path('add_topic/', login_required(views.AddTopicView.as_view()), name='add_topic'),
    path('topic<int:pk>/', views.TopicView.as_view(), name='topic'),
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('add_avatar/', login_required(views.AvatarAddView.as_view()), name='add_avatar'),
    path('grade<int:pk>/', login_required(views.GradeRiseCommentView.as_view()), name='plus_comment'),
    path('edit_post<int:pk>/', views.EditPostVies.as_view(), name='edit_post'),
    path('delete_post<int:pk>/', views.DeletePost.as_view(), name='delete_post'),
    path('grade_minus<int:pk>/', login_required(views.GradeMinusComment.as_view()), name='minus_comment'),
    path('delete_topic<int:pk>/', views.DeleteTopic.as_view(), name='delete_topic'),
    path('edit_topic<int:pk>/', views.EditTopic.as_view(), name='edit_topic')
]
