#!/usr/bin/env python
#coding=utf-8

# @file account.py
# @brief account
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13
from __future__ import unicode_literals

from django.db import models
from config import *

from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from signals import *
import django.utils.timezone as timezone
import json

class UserModel(User):
    class Meta:
        app_label = 'qr_gift'
    level=models.ForeignKey(SiteLevelConfigModel,null=True)
    exp=models.IntegerField(default=0);
    nick=models.CharField(max_length=256,default=u"路人甲")
    detailed_info=models.TextField(default="")
    registered_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    last_login_at=models.DateTimeField(default = timezone.now)
    card_count=models.IntegerField(default=0)
    subscribe_count=models.IntegerField(default=0)
    be_subscribe_count=models.IntegerField(default=0)

    objects = UserManager()
    def __unicode__(self):
        return self.username
    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))
