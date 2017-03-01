from django.shortcuts import render, redirect
from blog.models import Post, SubscribeUserInfo
from django.views.generic.list import ListView, View
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

def check_for_subscribe_existing(user):
    try:
        SubscribeUserInfo.objects.get(person=user)
    except:
        SubscribeUserInfo(person=user).save()


class AuthorCreate(CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):

             user = self.request.user
             form.instance.author = user
             return super(AuthorCreate, self).form_valid(form)


class FeedList(ListView):
    template_name = 'blog/feed_list.html'

    def get_queryset(self):

        posts_list = []
        check_for_subscribe_existing(self.request.user)
        for user in SubscribeUserInfo.objects.get(person_id=self.request.user.id).followed_users.all():
            for post in Post.objects.filter(author=user):
                post.read = post in self.request.user.is_read.all()
                posts_list.append(post)
        return sorted(posts_list, key=lambda x: x.datetime, reverse=True)


class UserBlogList(ListView):
    template_name = 'blog/blog_page.html'

    def get_context_data(self, **kwargs):

        self.publisher =self.args[0]
        context = super(UserBlogList, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.publisher)
        context['is_followed'] = User.objects.get(id=self.publisher) in SubscribeUserInfo.objects.get(
                                 person_id=self.request.user.id).followed_users.all()
        return context

    def get_queryset(self):

        self.publisher =self.args[0]
        user = User.objects.get(id=self.publisher)
        return Post.objects.filter(author=user)


class FollowView(View):

    def post(self, form):

        follow_id = self.request.POST.get('follow', False)
        user = User.objects.get(id=follow_id)
        if follow_id:
            check_for_subscribe_existing(self.request.user)
            sub = SubscribeUserInfo.objects.get(person=self.request.user)
            if user not in sub.followed_users.all():
                sub.followed_users.add(user)
            else:
                sub.followed_users.remove(user)
                for post in Post.objects.filter(author=user):
                    if post in self.request.user.is_read.all():
                        self.request.user.is_read.remove(post)
            print(sub.followed_users.all())
        return redirect('/users/{}'.format(follow_id))

class ReadPostView(View):

    def post(self, form):

        post_id = self.request.POST.get('post_id', False)
        if Post.objects.get(id=post_id) in self.request.user.is_read.all():
            self.request.user.is_read.remove(Post.objects.get(id=post_id))
        else:
            self.request.user.is_read.add(Post.objects.get(id=post_id))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
