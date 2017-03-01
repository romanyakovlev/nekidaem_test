from django.shortcuts import render, redirect
from blog.models import Post, SubscribeUserInfo
from django.views.generic.list import ListView, View
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Create your views here.

class FeedList(ListView):

    template_name = 'blog/feed_list.html'

    def get_queryset(self):
        posts_list = []
        print(SubscribeUserInfo.objects.get(person_id=self.request.user.id).followed_users.all())
        for x in SubscribeUserInfo.objects.get(person_id=self.request.user.id).followed_users.all():
            posts_list.append(*Post.objects.filter(author=x))

        return posts_list

class UserBlogList(ListView):

    template_name = 'blog/blog_page.html'

    def get_context_data(self, **kwargs):
        self.publisher =self.args[0]
        context = super(UserBlogList, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.publisher)
        context['is_followed'] = User.objects.get(id=self.publisher) in
            SubscribeUserInfo.objects.get(person_id=self.request.user.id).followed_users.all()
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
                sub = SubscribeUserInfo.objects.get(person=user)
                if self.request.user not in sub.followed_users.all():
                    sub.followed_users.add(self.request.user)
                else:
                    sub.followed_users.remove(self.request.user)
        return redirect('/users/{}'.format(follow_id))
