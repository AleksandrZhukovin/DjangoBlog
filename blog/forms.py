from django import forms
from django.core.validators import EmailValidator


class Registration(forms.Form):
    name = forms.CharField()
    email = forms.CharField(validators=[EmailValidator])
    password = forms.CharField(widget=forms.PasswordInput)


class LogIn(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddTopic(forms.Form):
    name = forms.CharField()
    text = forms.CharField()


class AddPost(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": "3"}))


