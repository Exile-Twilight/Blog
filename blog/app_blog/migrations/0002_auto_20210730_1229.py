# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-07-30 04:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, '正常'), (0, '删除'), (2, '草稿')], default=1, verbose_name='状态'),
        ),
        migrations.RemoveField(
            model_name='post',
            name='tag',
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(to='app_blog.Tag', verbose_name='标签'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, '正常'), (0, '删除')], default=1, verbose_name='状态'),
        ),
    ]
