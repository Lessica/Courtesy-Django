# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qr_gift', '0007_auto_20160222_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrstylemodel',
            name='style_border_binary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='style_border_res', to='qr_gift.CommonResourceModel'),
        ),
    ]
