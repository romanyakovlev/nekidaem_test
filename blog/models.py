from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User)
    datetime = models.DateTimeField(u'Дата публикации')
    content = models.TextField(max_length=10000)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return 'users/{}/blog/{}'.format(self.author.id, self.id)

class SubscribeUser(models.Model):
    user = models.OneToOneField(User)
    posts = models.ManyToManyField(Post)
