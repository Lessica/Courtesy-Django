# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 15:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import qr_gift.models.config


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        ('qr_gift', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardModel',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=32)),
                ('is_public', models.BooleanField()),
                ('visible_at', models.DateTimeField()),
                ('first_read_at', models.DateTimeField()),
                ('view_count', models.IntegerField()),
                ('is_editable', models.BooleanField()),
                ('edited_count', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('stars', models.IntegerField()),
                ('banned', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='QRCodeModel',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('channel', models.IntegerField()),
                ('unique_id', models.CharField(max_length=16, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_recorded', models.BooleanField()),
                ('recorded_at', models.DateTimeField()),
                ('scan_count', models.IntegerField()),
                ('card_token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qr_gift.CardModel')),
            ],
        ),
        migrations.CreateModel(
            name='QRStyleModel',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=256)),
                ('preview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preview_res', to='qr_gift.CommonResourceModel')),
                ('style_binary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='style_binary_id_res', to='qr_gift.CommonResourceModel')),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfigCategoryModel',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('description', models.TextField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfigModel',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=256, unique=True)),
                ('value', models.CharField(max_length=256)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('category', models.FloatField(verbose_name=qr_gift.models.config.SiteConfigCategoryModel)),
            ],
        ),
        migrations.CreateModel(
            name='SiteLevelConfigModel',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('level', models.IntegerField(default=1, unique=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('min_exp', models.IntegerField()),
                ('max_exp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TemplateModel',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('enabled', models.BooleanField()),
                ('has_text_area', models.BooleanField()),
                ('max_text_length', models.IntegerField()),
                ('has_image_area', models.BooleanField()),
                ('max_image_length', models.IntegerField()),
                ('has_audio_area', models.BooleanField()),
                ('has_video_area', models.BooleanField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('preview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pre_res', to='qr_gift.CommonResourceModel')),
                ('style_binary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='style_res', to='qr_gift.CommonResourceModel')),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('exp', models.IntegerField(default=0)),
                ('detailed_info', models.TextField(default='')),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('last_login_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('card_count', models.IntegerField(default=0)),
                ('subscribe_count', models.IntegerField(default=0)),
                ('be_subscribe_count', models.IntegerField(default=0)),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='qr_gift.SiteLevelConfigModel')),
            ],
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='qrcodemodel',
            name='style',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qr_gift.QRStyleModel'),
        ),
        migrations.AddField(
            model_name='cardmodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_usermodel', to='qr_gift.UserModel'),
        ),
        migrations.AddField(
            model_name='cardmodel',
            name='read_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_by_usermodel', to='qr_gift.UserModel'),
        ),
        migrations.AddField(
            model_name='cardmodel',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qr_gift.TemplateModel'),
        ),
    ]
