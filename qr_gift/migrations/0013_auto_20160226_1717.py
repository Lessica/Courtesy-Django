# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-26 09:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qr_gift', '0012_auto_20160225_2205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='constellation',
            new_name='area',
        ),
    ]