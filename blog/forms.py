from django import forms
from .models import Topic, Post, User, Avatar
from django.contrib.auth.forms import UserCreationForm


class LogIn(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


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
        fields = ['avatar']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
