from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User)
    datetime = models.DateTimeField(u'Дата публикации', auto_now_add=True, blank=True)
    content = models.TextField(max_length=10000)
    is_read = models.ForeignKey(User, related_name='is_read', null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            send_mail('Пользователь {} выложил новый пост'.format(self.author),
                '{}'.format(self.title), settings.EMAIL_HOST_USER,
                [self.author.email], fail_silently=False)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/users/{}'.format(self.author.id)


class SubscribeUserInfo(models.Model):
    person= models.OneToOneField(User)
    followed_users = models.ManyToManyField(User, related_name='follows')
