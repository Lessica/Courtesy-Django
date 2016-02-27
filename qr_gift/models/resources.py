#!/usr/bin/env python
#coding=utf-8

# @file resources.py
# @brief resources
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13

from __future__ import unicode_literals

from django.db import models
class CommonResourceModel(models.Model):
    class Meta:
        app_label = 'qr_gift'
    id=models.AutoField(primary_key=True,editable=False)
    #  origin_url=models.URLField()
    #  cdn_url=models.URLField(null=True)
    id_md5=models.CharField(max_length=32,default="")
    kind=models.CharField(max_length=4,default="")
    uploaded_at=models.DateTimeField(auto_now_add=True)
    def toDict(self):
        ret={
            "id":self.id,
            "origin_url":self.origin_url,
        }
        return ret

class AvatarImageModel(CommonResourceModel):
    class Meta:
        app_label = 'qr_gift'
    size=models.IntegerField()

