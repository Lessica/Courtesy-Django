# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 02:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_gift', '0002_auto_20160221_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='nick',
            field=models.CharField(default=0, max_length=256),
            preserve_default=False,
        ),
    ]
