from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import LogIn, AddTopic, AddPost, AddAvatar
from .models import User, Topic, Post, Avatar
# from django.contrib.auth.models import Group
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView


class HomeView(ListView):
    model = Topic
    template_name = 'index.html'
    context_object_name = 'topics'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['user'] = self.request.user
        return context


class RegistrationView(CreateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = 'registration.html'
    success_url = reverse_lazy('index')


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LogIn
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data['name']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log In'
        return context


class LogoutView(RedirectView):
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class AddTopicView(CreateView):
    template_name = 'add_topic.html'
    model = Topic
    form_class = AddTopic
    success_url = reverse_lazy('index')

    @method_decorator(login_required)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Topic'
        return context


class TopicView(CreateView):
    model = Post
    template_name = 'topic.html'
    form_class = AddPost

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.topic = Topic.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Topic'
        context['comments'] = Post.objects.filter(topic=Topic.objects.get(id=self.kwargs['pk']))
        return context

    def get_success_url(self):
        return f'/topic{self.kwargs["pk"]}'


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.request.user.username} Profile'
        context['user'] = self.request.user
        context['avatar'] = Avatar.objects.get(user=self.request.user.id)
        return context


class AvatarAddView(CreateView):
    model = Avatar
    template_name = 'add_avatar.html'
    form_class = AddAvatar
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
