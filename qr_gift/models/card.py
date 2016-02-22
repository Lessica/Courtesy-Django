#!/usr/bin/env python
#coding=utf-8

# @file card.py
# @brief card
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13
from __future__ import unicode_literals

from django.db import models

from resources import *
from account import *

class TemplateModel(models.Model):
    class Meta:
        app_label = 'qr_gift'
    id=models.IntegerField(primary_key=True,editable=False)
    style_binary=models.ForeignKey(CommonResourceModel,related_name='style_res')
    preview=models.ForeignKey(CommonResourceModel,related_name='pre_res')
    enabled=models.BooleanField()
    has_text_area=models.BooleanField()
    max_text_length=models.IntegerField()
    has_image_area=models.BooleanField()
    max_image_length=models.IntegerField()
    has_audio_area=models.BooleanField()
    has_video_area=models.BooleanField()
    create_at=models.DateTimeField(auto_now_add=True)

class CardModel(models.Model):
    class Meta:
        app_label = 'qr_gift'
    id=models.IntegerField(primary_key=True,editable=False)
    template=models.ForeignKey(TemplateModel)
    author=models.ForeignKey(UserModel,related_name='author_usermodel')
    read_by=models.ForeignKey(UserModel,related_name='read_by_usermodel')
    token=models.CharField(max_length=32)
    is_public=models.BooleanField()
    visible_at=models.DateTimeField()
    first_read_at=models.DateTimeField()
    view_count=models.IntegerField()
    is_editable=models.BooleanField()
    edited_count=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    stars=models.IntegerField()
    banned=models.BooleanField()

