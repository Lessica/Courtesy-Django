#!/usr/bin/env python
#coding=utf-8

# @file config.py
# @brief config
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13
from __future__ import unicode_literals

from django.db import models

class SiteLevelConfigModel(models.Model):
    class Meta:
        app_label = 'qr_gift'
    id=models.IntegerField(primary_key=True,editable=False)
    level=models.IntegerField(unique=True,default=1)
    name=models.CharField(max_length=256,unique=True)
    min_exp=models.IntegerField()
    max_exp=models.IntegerField()

class SiteConfigCategoryModel(models.Model):
    class Meta:
        app_label = 'qr_gift'
    id=models.IntegerField(primary_key=True,editable=False)
    name=models.CharField(max_length=256,unique=True)
    description=models.TextField()
    create_at=models.DateTimeField(auto_now_add=True)

class SiteConfigModel(models.Model):
    class Meta:
        app_label = 'qr_gift'
    id=models.IntegerField(primary_key=True,editable=False)
    key=models.CharField(max_length=256,unique=True)
    value=models.CharField(max_length=256);
    modified_at=models.DateTimeField(auto_now=True)
    description=models.TextField()
    category=models.FloatField(SiteConfigCategoryModel)
