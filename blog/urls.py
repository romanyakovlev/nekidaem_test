from django.conf.urls import url, include
from django.contrib import admin
from blog.views import FeedList, UserBlogList, FollowView, ReadPostView, AuthorCreate


urlpatterns = [
    url(r'^feed/$', FeedList.as_view()),
    url(r'^read_post/$', ReadPostView.as_view()),
    url(r'users/(\d+)/$', UserBlogList.as_view()),
    url(r'^follow/$', FollowView.as_view()),
    url(r'^create_post/$', AuthorCreate.as_view()),
]
