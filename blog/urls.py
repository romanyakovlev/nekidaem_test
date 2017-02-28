from django.conf.urls import url, include
from django.contrib import admin
from blog.views import UserBlogList, BlogPostsList


urlpatterns = [
    url(r'^myblog/$', BlogPostsList.as_view()),
    url(r'users/(\d+)/$', UserBlogList.as_view()),
]
