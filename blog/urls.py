from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_page, name='login'),
    path('test/', views.test, name='test'),
    path('logout/', views.logout_page, name='logout'),
    path('add_topic/', views.add_topic, name='add_topic'),
    path('topic<int:topic_id>/', views.topic, name='topic')
]
