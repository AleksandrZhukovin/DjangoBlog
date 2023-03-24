from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import AddTopic, AddPost, AddAvatar, RegistrationForm
from .models import Topic, Post, Avatar, Level, Like
from django.contrib.auth.models import Group
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import os


class HomeView(ListView):
    model = Topic
    template_name = 'index.html'
    context_object_name = 'topics'

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['user'] = user
        if user.is_authenticated:
            obj, created = Level.objects.get_or_create(user=user)

        if user.is_authenticated and len(user.groups.all()) == 0:
            user.groups.add(Group.objects.get(name='Green Apples'))
        if user.is_authenticated:
            level = Level.objects.get(user=user)
            likes = Like.objects.filter(user=user)
            if 5 <= level.answer < 30 and 2 <= len(likes) < 50:
                user.groups.clear()
                user.groups.add(Group.objects.get(name='Growing Up Puppy'))

            if level.answer >= 30 and 50 <= len(likes) == 50:
                user.groups.clear()
                user.groups.add(Group.objects.get(name='Sensei'))

        return context


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context


class Login(LoginView):
    template_name = 'login.html'

    redirect_authenticated_user = True
    extra_context = {'title': 'Log In'}


class Logout(LogoutView):
    pass


class AddTopicView(CreateView):
    template_name = 'add_topic.html'
    model = Topic
    form_class = AddTopic
    success_url = reverse_lazy('index')

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
        level = Level.objects.get(user=self.request.user)
        level.answer += 1
        level.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['title'] = 'Topic'
        context['user'] = self.request.user
        try:
            context['avatar'] = Avatar.objects
        except Avatar.DoesNotExist:
            context['avatar'] = None
        context['topic'] = Topic.objects.get(id=pk)

        try:
            context['creator_avatar'] = Avatar.objects.get(user=Topic.objects.get(id=pk).user).file.url
        except Avatar.DoesNotExist:
            context['creator_avatar'] = None

        posts = []
        n = 0
        for p in Post.objects.filter(topic=Topic.objects.get(id=pk)):
            p.grade = len(Like.objects.filter(post=p))
            posts.append([p])
            posts[n].append([i.user for i in Like.objects.filter(user=self.request.user.id, post=p)])
            n += 1
        context['posts'] = posts
        return context

    def get_success_url(self):
        return f'/topic{self.kwargs["pk"]}'


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['title'] = f'{user.username} Profile'
        context['user'] = user
        context['level'] = Level.objects.get(user=user)
        context['likes'] = len(Like.objects.filter(user=user))
        try:
            context['avatar'] = Avatar.objects.get(user=user.id).file.url
        except Avatar.DoesNotExist:
            context['avatar'] = None
        context['topics'] = Topic.objects.filter(user=user)
        return context


class AvatarAddView(CreateView):
    model = Avatar
    template_name = 'add_avatar.html'
    form_class = AddAvatar
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Avatar'
        return context

    def form_valid(self, form):
        avatars = Avatar.objects.all()
        for a in avatars:
            if a.user.id == self.request.user.id:
                os.remove(a.avatar.path.replace(os.sep, '/'))
                a.delete()
        form.instance.user = self.request.user
        return super().form_valid(form)


class GradeRiseCommentView(UpdateView):
    model = Post
    fields = []

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['pk'])
        post.grade += 1
        post.save()
        like = Like(post=post, user=self.request.user)
        like.save()
        return redirect(f'/topic{post.topic.id}/')


class GradeMinusComment(UpdateView):
    model = Post
    fields = []

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['pk'])
        like = Like.objects.get(post=post, user=self.request.user)
        like.delete()
        return redirect(f'/topic{post.topic.id}/')


class EditPostVies(UpdateView):
    model = Post
    fields = ['body']
    template_name = 'edit_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        user = self.request.user
        context['title'] = 'Edit Post'
        context['post_e'] = Post.objects.get(id=pk)
        context['user'] = user

        try:
            context['avatar'] = Avatar.objects.get(user=user.id).file.url
        except Avatar.DoesNotExist:
            context['avatar'] = None
        context['topic'] = Post.objects.get(id=pk).topic

        try:
            context['creator_avatar'] = Avatar.objects.get(user=Post.objects.get(id=pk).topic.user).file.url
        except Avatar.DoesNotExist:
            context['creator_avatar'] = None

        posts = []
        n = 0
        for p in Post.objects.filter(topic=Post.objects.get(id=pk).topic):
            p.grade = len(Like.objects.filter(user=user.id, post=p))
            posts.append([p])
            posts[n].append([i.user for i in Like.objects.filter(user=user.id, post=p)])
            n += 1
        context['posts'] = posts
        return context

    def get_success_url(self):
        return f'/topic{Post.objects.filter(topic=Post.objects.get(id=self.kwargs["pk"]).topic)[0].topic.id}/'


class DeletePost(DeleteView):
    model = Post
    template_name = 'delete_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context

    def get_success_url(self):
        return f'/topic{Post.objects.filter(topic=Post.objects.get(id=self.kwargs["pk"]).topic)[0].topic.id}/'


class DeleteTopic(DeleteView):
    model = Topic
    template_name = 'delete_topic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Topic'
        return context

    def form_valid(self, form):
        for p in Post.objects.filter(id=self.kwargs['pk']):
            p.delete()
        return super().form_valid(form)

    def get_success_url(self):
        return f'/profile/'


class EditTopic(UpdateView):
    model = Topic
    template_name = 'edit_topic.html'
    form_class = AddTopic
    success_url = '/profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = Topic.objects.get(id=self.kwargs['pk'])
        self.initial = {'name': topic.name, 'text': topic.text}
        context['title'] = 'Edit Topic'
        return context
