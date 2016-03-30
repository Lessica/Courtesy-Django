#!/usr/bin/env python
#coding=utf-8

# @file qrcode.py
# @brief qrcode
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13

from django.core.exceptions import *
from django.db import IntegrityError

from models.qr import *
from models.account import *
import hashlib
import datetime
import time

def qr_query(request,post_data,ret):
    qr_id=post_data["qr_id"]
    try:
        qr_model=QRCodeModel.objects.get(unique_id=qr_id)
    except ( ValueError,ObjectDoesNotExist ):
        ret["error"]=423
        return ret
    ret["qr_info"]=qr_model.toDict()
    qr_model.scan_count=qr_model.scan_count+1
    #  if qr_model.is_recorded==True:
        #  card=qr_model.card_token
        #  ret["card_info"]=card.toDict()
        #  if not request.user.is_authenticated():
            #  card.view_count=card.view_count+1
            #  if not card.first_read_at:
                #  card.read_by_id=request.user.id
            #  card.save()

        #  elif request.user.id!=card.author_id:
            #  card.view_count=card.view_count+1
            #  if not card.first_read_at:
                #  card.read_by_id=request.user.id
                #  card.first_read_at=datetime.datetime.now()

            #  card.save()
    qr_model.save()

    return ret

def card_query(request,post_data,ret):
    try:
        card=CardModel.objects.get(token=post_data["token"])
    except ( ValueError,ObjectDoesNotExist ):
        ret["error"]=404
        return ret
    except KeyError:
        ret["error"]=401
        return ret
    ##TODO
    if card.banned:
        ret["error"]=425
        return ret

    if not request.user.is_authenticated():
        card.view_count=card.view_count+1
        if not card.first_read_at:
            card.first_read_at=datetime.datetime.now()
        card.save()

    elif request.user.id!=card.author_id:
        card.view_count=card.view_count+1
        if not card.first_read_at:
            card.read_by_id=request.user.id
            card.first_read_at=datetime.datetime.now()
        card.save()
    ret["card_info"]=card.toDict()

    if card.visible_at>datetime.datetime.now():
        ret["card_info"]["local_template"]=None
    return ret

def card_edit(request,post_data,ret):
    if not request.user.is_authenticated():
        ret["error"]=403
        return ret
    card_info=post_data["card_info"]
    try:
        card=CardModel.objects.get(token=post_data["token"])
    except ( ValueError,ObjectDoesNotExist ):
        ret["error"]=404
        return ret
    ##TODO
    #  card.author=UserModel.objects.get(user_ptr_id=request.user.id)
    if request.user.id!=card.author_id:
        ret["error"]=425
        return ret
    if card.banned:
        ret["error"]=425
        return ret
    card.local_template=card_info["local_template"]
    card.is_public=card_info["is_public"]
    card.is_editable=card_info["is_editable"]
    card.visible_at=datetime.datetime.fromtimestamp(card_info["visible_at"])
    card.edited_count=card.edited_count+1
    card.save()
    ret["card_info"]=card.toDict()
    return ret

def card_create(request,post_data,ret):
    if not request.user.is_authenticated():
        ret["error"]=403
        return ret
    card_info=post_data["card_info"]
    qr_code=QRCodeModel.objects.get(unique_id=post_data["qr_id"])
    if qr_code.is_recorded:
        ret["error"]=424
        return ret

    new_card=CardModel()
    new_card.author=UserModel.objects.get(user_ptr_id=request.user.id)
    new_card.local_template=card_info["local_template"]
    new_card.is_public=card_info["is_public"]
    new_card.is_editable=card_info["is_editable"]
    new_card.token=hashlib.md5(post_data["qr_id"]).hexdigest()
    new_card.visible_at=datetime.datetime.fromtimestamp(card_info["visible_at"])
    new_card.save()

    qr_code.is_recorded=True
    qr_code.recorded_at=str(datetime.datetime.now())
    qr_code.card_token=new_card
    qr_code.save()
    ret["card_info"]=new_card.toDict()
    return ret

