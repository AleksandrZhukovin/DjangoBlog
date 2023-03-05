from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import Registration, LogIn, AddTopic, AddPost
from .models import User, Topic, Post


def index(request):
    user = request.user
    topics = Topic.objects.all()

    context = {
        'title': "Home",
        'user': user,
        'topics': topics
    }
    return render(request, 'index.html', context)


def registration(request):
    if request.method == "POST":
        form = Registration(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(name, email, password)
            user.save()

    else:
        form = Registration()

    context = {
        'title': 'Sign Up',
        'form': form
    }
    return render(request, 'registration.html', context)


def login_page(request):
    if request.method == "POST":
        form = LogIn(request.POST)

        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = LogIn()

    context = {
        'title': 'Log In',
        'form': form
    }
    return render(request, 'login.html', context)


@login_required
def test(request):
    context = {
        'title': 'Test',
        'val': 'IT IS OK'
    }
    return render(request, 'test.html', context)


def logout_page(request):
    logout(request)
    return redirect('/')


@login_required
def add_topic(request):
    user = request.user
    if request.method == "POST":
        form = AddTopic(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']
            user = request.user
            t = Topic(name=name, text=text, user=user)
            t.save()
            return redirect('/')
    else:
        form = AddTopic()
    context = {
        'title': 'Add Topic',
        'user': user,
        'form': form
    }
    return render(request, 'add_topic.html', context)


def topic(request, topic_id):
    t = Topic.objects.get(id=topic_id)
    comments = Post.objects.filter(topic=t)
    if request.method == "POST":
        form = AddPost(request.POST)
        if form.is_valid():
            post = form.cleaned_data['text']
            p = Post(body=post, topic=t, user=request.user)
            p.save()
    else:
        form = AddPost()
    context = {
        'form': form,
        'title': t.name,
        'comments': comments,
        'topic': t
    }
    return render(request, 'topic.html', context)
