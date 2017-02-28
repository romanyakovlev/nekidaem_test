from django.shortcuts import render
from blog.models import Post, SubscribeUser
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

# Create your views here.

class UserBlogList(ListView):

    template_name = 'blog/user_blog.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserBlogList, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        self.publisher =self.args[0]
        return Post.objects.filter(author_id=self.publisher)

class BlogPostsList(ListView):

    template_name = 'blog/user_blog.html'

    def get_queryset(self):
        try:
            return SubscribeUser.objects.get(user=self.request.user).posts.all()
        except:
            return None
