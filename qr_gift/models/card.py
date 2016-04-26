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
import datetime
import time
import json


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
    #  id=models.IntegerField(primary_key=True,editable=False)
    template=models.ForeignKey(TemplateModel,null=True)
    local_template=models.TextField(null=True)
    author=models.ForeignKey(UserModel,related_name='author_usermodel')
    read_by=models.ForeignKey(UserModel,related_name='read_by_usermodel',null=True)
    token=models.CharField(max_length=32,unique=True)
    is_public=models.BooleanField()
    visible_at=models.DateTimeField()
    first_read_at=models.DateTimeField(null=True)
    view_count=models.IntegerField(default=0)
    is_editable=models.BooleanField()
    edited_count=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    stars=models.IntegerField(default=0)
    banned=models.BooleanField(default=False)
    def toDict(self):
        dic={
            "author":self.author.toDict(),
            "token":self.token,
            "is_public":self.is_public,
            "view_count":self.view_count,
            "is_editable":self.is_editable,
            "edited_count":self.edited_count,
            "created_at":int(str(time.mktime(self.created_at.timetuple()))[:-2]),
            "modified_at":int(str(time.mktime(self.modified_at.timetuple()))[:-2]),
            "stars":self.stars,
            "visible_at":int(str(time.mktime(self.visible_at.timetuple()))[:-2]),
            "local_template":json.loads( self.local_template ),
        }

        if self.read_by:
            dic["read_by"]=self.read_by.toDict()

        if self.first_read_at:
            dic["first_read_at"]=int(str(time.mktime(self.first_read_at.timetuple()))[:-2])
            #  print dic
        else:
            dic["first_read_at"]=self.first_read_at
        #  tz_info = self.visible_at.tzinfo
        #  if time.mktime(self.visible_at.timetuple())>time.time():
        return dic


