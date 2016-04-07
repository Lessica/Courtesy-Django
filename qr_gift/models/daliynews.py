#!/usr/bin/env python
#coding=utf-8

# @file daliynews.py
# @brief daliynews
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13
from __future__ import unicode_literals

from django.db import models
from resources import *

class DaliyNewsStyleModel(models.Model):
    class Meta:
        app_label = 'qr_gift'
    style_name=models.CharField(max_length=16)

    def __unicode__(self):
        return self.style_name
    def toDict(self):
        ret={
            'style_id':self.id,
            'style_name':self.style_name,
            }
        return ret

class DaliyNewsModel(models.Model):
    class Meta:
        app_label = 'qr_gift'

    image=models.ForeignKey(CommonResourceModel,related_name='image_res',null=True)
    video=models.ForeignKey(CommonResourceModel,related_name='video_res',null=True)
    audio=models.ForeignKey(CommonResourceModel,related_name='voice_res',null=True)
    date_str=models.CharField(max_length=16)
    string=models.TextField(null=True)
    style=models.ForeignKey(DaliyNewsStyleModel,null=True)
    def __unicode__(self):
        return self.date_str

    def toDict(self):
        ret={
            'image':self.image.toDict(),
            'video':None if self.video==None else self.video.toDict(),
            'audio':None if self.audio==None else self.audio.toDict(),
            'date':self.date_str,
            'string':self.string,
            'style':self.style.toDict(),
        }
        return ret

