from django import forms
from .models import Topic, Post, User, Avatar
from django.contrib.auth.forms import UserCreationForm


class AddTopic(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'text']


class AddPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']


class AddAvatar(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['file']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
