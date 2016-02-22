#!/usr/bin/env python
#coding=utf-8

# @file qr.py
# @brief qr
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13

from __future__ import unicode_literals

from django.db import models
from resources import *
from card import *

class QRStyleModel(models.Model):
    class Meta:
        app_label = 'qr_gift'
    id=models.IntegerField(primary_key=True,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=256)
    style_binary=models.ForeignKey(CommonResourceModel,related_name='style_binary_id_res')
    preview=models.ForeignKey(CommonResourceModel,related_name='preview_res')

class QRCodeModel(models.Model):
    class Meta:
        app_label = 'qr_gift'
    id=models.IntegerField(primary_key=True,editable=False)
    channel=models.IntegerField()
    style=models.ForeignKey(QRStyleModel)
    unique_id=models.CharField(max_length=16,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_recorded=models.BooleanField()
    recorded_at=models.DateTimeField()
    scan_count=models.IntegerField()
    card_token=models.OneToOneField(CardModel)
