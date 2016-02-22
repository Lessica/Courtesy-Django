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
    id=models.IntegerField(primary_key=True,editable=False)
    origin_url=models.URLField()
    cdn_url=models.URLField()
    uploaded_at=models.DateTimeField(auto_now_add=True)

class AvatarImageModel(CommonResourceModel):
    class Meta:
        app_label = 'qr_gift'
    size=models.IntegerField()

