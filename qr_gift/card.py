#!/usr/bin/env python
#coding=utf-8

# @file card.py
# @brief card
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13

from models.card import *
from models.qr import *
from models.account import *

from commonupload import *
import datetime
import shutil
import json
import traceback

ORI_PATH="/home/ursync"

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

def card_edit_query(request,post_data,ret):
    if not request.user.is_authenticated():
        ret["error"]=403
        return ret
    card_info=post_data["card_info"]

    try:
        card=CardModel.objects.get(token=card_info["token"])
    except ( ValueError,ObjectDoesNotExist ):
        ret["error"]=404
        return ret

    if request.user.id!=card.author_id:
        ret["error"]=425
        return ret

    return ret

def card_edit(request,post_data,ret):
    if not request.user.is_authenticated():
        ret["error"]=403
        return ret
    card_info=post_data["card_info"]
    try:
        card=CardModel.objects.get(token=card_info["token"])
    except ( ValueError,ObjectDoesNotExist ):
        ret["error"]=404
        return ret

    try:
        shutil.rmtree(join("qr_gift","static","card",card_info["token"]))
        shutil.copytree(join(ORI_PATH,card_info["token"]),join("qr_gift","static","card",card_info["token"]))

    except Exception,e:
        ret["error"]=430
        return ret

    ##TODO
    #  card.author=UserModel.objects.get(user_ptr_id=request.user.id)
    if request.user.id!=card.author_id:
        ret["error"]=425
        return ret
    #  if card.banned:
        #  ret["error"]=425
        #  return ret
    card.local_template=json.dumps( card_info["local_template"] )
    card.is_public=True
    card.banned=card_info["is_banned"]
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


    flag=0
    card_info=post_data["card_info"]

    try:
        shutil.copytree(join(ORI_PATH,card_info["token"]),join("qr_gift","static","card",card_info["token"]))
    except Exception,e:
        if "File exists" in e:
            shutil.rmtree(join("qr_gift","static","card",card_info["token"]))
            shutil.copytree(join(ORI_PATH,card_info["token"]),join("qr_gift","static","card",card_info["token"]))
        else:
            traceback.print_exc()
            ret["error"]=430
            return ret

    if "qr_id" in card_info.keys():
        flag=1
        qr_code=QRCodeModel.objects.get(unique_id=card_info["qr_id"])
        if qr_code.is_recorded:
            ret["error"]=424
            return ret

    new_card=CardModel()
    new_card.author=UserModel.objects.get(user_ptr_id=request.user.id)
    new_card.local_template=json.dumps( card_info["local_template"] )
    new_card.is_public=True
    new_card.banned=card_info["is_banned"]
    new_card.is_editable=card_info["is_editable"]
    #  new_card.token=hashlib.md5(post_data["qr_id"]).hexdigest()
    new_card.token=card_info["token"]
    new_card.visible_at=datetime.datetime.fromtimestamp(card_info["visible_at"])

    new_card.save()

    if flag==1:
        qr_code.is_recorded=True
        qr_code.recorded_at=str(datetime.datetime.now())
        qr_code.card_token=new_card
        qr_code.save()

    ret["card_info"]=new_card.toDict()

    return ret

def card_create_query(request,post_data,ret):
    if not request.user.is_authenticated():
        ret["error"]=403
        return ret
    card_info=post_data["card_info"]
    if "qr_id" in card_info.keys():
        qr_code=QRCodeModel.objects.get(unique_id=card_info["qr_id"])
        if qr_code.is_recorded:
            ret["error"]=424
            return ret
    if CardModel.objects.filter(token=card_info["token"]).exists():
        ret["error"]=434
        return ret
    #TODO
    #check something
    #need session

    ret["token"]=card_info["token"]
    return ret

def card_ban(request,post_data,ret):
    if not request.user.is_authenticated():
        ret["error"]=403
        return ret

    try:
        card=CardModel.objects.get(token=post_data["token"])
    except ( ValueError,ObjectDoesNotExist ):
        ret["error"]=404
        return ret
    except KeyError:
        ret["error"]=401
        return ret

    if request.user.id!=card.author_id:
        ret["error"]=425
        return ret
    card.banned=True
    card.save()
    ret["token"]=post_data["token"]
    return ret
def card_restore(request,post_data,ret):
    if not request.user.is_authenticated():
        ret["error"]=403
        return ret

    try:
        card=CardModel.objects.get(token=post_data["token"])
    except ( ValueError,ObjectDoesNotExist ):
        ret["error"]=404
        return ret
    except KeyError:
        ret["error"]=401
        return ret

    if request.user.id!=card.author_id:
        ret["error"]=425
        return ret
    card.banned=False
    card.save()
    ret["token"]=post_data["token"]
    return ret


class CardResourceUpload(CommonUpload):
    def __init__(self,request,ret):
        self.request=request
        self.ret=ret
    class UploadForm(forms.Form):
        card_res=forms.FileField(required=True)
    def upload(self,uf):
        [id_md5,server_path,kind]=handle_uploaded_file(self.request.FILES['card_res'],str(time.time()),"card_res")
        url_path=server_path[7:]
        res=CommonResourceModel(id_md5=id_md5,kind=kind,sha_256=file2sha256(server_path))
        res.save()
        self.ret["id"]=id_md5


