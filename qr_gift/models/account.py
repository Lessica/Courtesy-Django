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
import time
from resources import *

class UserModel(User):
    class Meta:
        app_label='qr_gift'
    level=models.ForeignKey(SiteLevelConfigModel,null=True)
    exp=models.IntegerField(default=0);
    detailed_info=models.TextField(default="")
    registered_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    #  last_login_at=models.DateTimeField(default = timezone.now)
    card_count=models.IntegerField(default=0)
    subscribe_count=models.IntegerField(default=0)
    be_subscribe_count=models.IntegerField(default=0)

    nick=models.CharField(max_length=256,default=u"路人甲")
    avatar=models.ForeignKey(CommonResourceModel,null=True,related_name="avater")
    banner=models.ForeignKey(CommonResourceModel,null=True,related_name="banner")
    mobile=models.CharField(max_length=16,default="")
    birthday=models.CharField(max_length=16,default="")
    gender=models.IntegerField(default=1)
    province=models.CharField(max_length=32,default="")
    city=models.CharField(max_length=32,default="")
    area=models.CharField(max_length=32,default="")
    #  constellation=models.CharField(max_length=32,default="")

    objects = UserManager()
    def __unicode__(self):
        return self.username
    def toDict(self):
        dic={
            "user_id":self.user_ptr_id,
            "email":self.email,
            "registered_at":int(str(time.mktime(self.registered_at.timetuple()))[:-2]),
            "last_login_at":int(str(time.mktime(self.last_login.timetuple()))[:-2]),
            "card_count":self.card_count,
            "profile":{
                "nick":self.nick,
                #  "avatar":self.avatar.id_md5,
                "mobile":self.mobile,
                "birthday":self.birthday,
                "gender":self.gender,
                "province":self.province,
                "city":self.city,
                "area":self.area,
                #  "constellation":self.constellation,
                "introduction":self.detailed_info,
            }
        }
        if self.avatar:
            dic["profile"]["avatar"]=self.avatar.id_md5
        if self.banner:
            dic["profile"]["banner"]=self.banner.id_md5
        return dic
