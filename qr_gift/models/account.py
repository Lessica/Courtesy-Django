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
from resources import *

class UserModel(User):
    class Meta:
        app_label = 'qr_gift'
    level=models.ForeignKey(SiteLevelConfigModel,null=True)
    exp=models.IntegerField(default=0);
    nick=models.CharField(max_length=256,default=u"路人甲")
    logo=models.ForeignKey(CommonResourceModel,null=True)
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
    def toDict(self):
        dic={
            "email":self.email,
            "nick":self.nick,
            "detailed_info":self.detailed_info,
            "level":self.level,
            "exp":self.exp,
            "registered_at":self.registered_at.strftime('%Y-%m-%d %H:%M:%S'),
            "modified_at":self.modified_at.strftime('%Y-%m-%d %H:%M:%S'),
            "last_login_at":self.last_login_at.strftime('%Y-%m-%d %H:%M:%S'),
            "card_count":self.card_count,
            "subscribe_count":self.subscribe_count,
            "be_subscribe_count":self.be_subscribe_count,
        }
        return dic
