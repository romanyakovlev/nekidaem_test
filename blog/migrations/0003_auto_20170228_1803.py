# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_subscribeuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribeuser',
            name='posts',
        ),
        migrations.AddField(
            model_name='subscribeuser',
            name='posts',
            field=models.ManyToManyField(to='blog.Post'),
        ),
    ]
