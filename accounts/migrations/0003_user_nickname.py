# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170727_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
