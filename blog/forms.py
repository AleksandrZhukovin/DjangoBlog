from django import forms
from .models import Topic, Post, User, Avatar


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