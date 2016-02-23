#!/usr/bin/env python
#coding=utf-8

# @file qr.py
# @brief qr
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13

from __future__ import unicode_literals

from django.db import models


from wsgiref.util import FileWrapper
import os, tempfile, zipfile

from resources import *
from card import *

class QRStyleModel(models.Model):
    class Meta:
        app_label = 'qr_gift'
    id=models.AutoField(primary_key=True,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=256,unique=True)
    style_border_binary=models.OneToOneField(CommonResourceModel,related_name='style_border_res',null=True)
    style_center_binary=models.OneToOneField(CommonResourceModel,related_name='style_center_res',null=True)
    style_script=models.OneToOneField(CommonResourceModel,related_name='style_script_res',null=True)
    preview=models.OneToOneField(CommonResourceModel,related_name='preview_res',null=True)
    def __unicode__(self):
        return self.name

class QRCodeModel(models.Model):
    class Meta:
        app_label = 'qr_gift'
    id=models.AutoField(primary_key=True,editable=False)
    channel=models.IntegerField()
    style=models.ForeignKey(QRStyleModel)
    unique_id=models.CharField(max_length=16,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_recorded=models.BooleanField(default=False)
    recorded_at=models.DateTimeField(null=True)
    scan_count=models.IntegerField(default=0)
    card_token=models.OneToOneField(CardModel,null=True)
    def __unicode__(self):
        return self.name

