from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django import forms
from django.core.exceptions import *

from .models import *
import re
import json
from wsgiref.util import FileWrapper
from os.path import join as jn
import zipfile
import time
from PIL import Image
import datetime
import os

import news
import user
import qrcode
import card

#######################################################
################## UPLOAD PART ########################
#######################################################
#TODO
def res_query(request,post_data,ret):
    sha_256=post_data["hash"]
    try:
        ret["res"]=CommonResourceModel.objects.get(sha_256=sha_256).toDict()
    except ( ValueError,ObjectDoesNotExist ):
        ret["error"]=404
    return ret


def common_upload(request,action):
    if not request.user.is_authenticated():
        ret={"error":403}
        return HttpResponse(json.dumps(ret), content_type="application/json")

    act2class={
        "avatar":user.UserAvatarUpload,
        "banner":user.UserBannerUpload,
        "qr_style":qrcode.QRStyleUpload,
        "card_res":card.CardResourceUpload,
        "news":news.DaliyNewsUpload,
    }
    ret={"error":0}
    common_upload_class=act2class[action](request,ret)
    common_upload_form=common_upload_class.UploadForm

    if request.method == "POST":
        uf = common_upload_form(request.POST,request.FILES)
        if uf.is_valid():
            common_upload_class.upload(uf)
            ret=common_upload_class.ret
        else:
            ret={"error":401}

        ret["time"]=int(round(time.time() * 1e3)/1e3)
        return HttpResponse(json.dumps(ret), content_type="application/json")
    else:
        uf = common_upload_form()
        return render_to_response('common_upload.html',{'uf':uf})


def common_download(request,action):
    if not request.user.is_authenticated():
        ret={"error":403}
        return HttpResponse(json.dumps(ret), content_type="application/json")

    act2class={
        "qr_arrise":qrcode.QRArriseDownload,
    }
    #  ret={"error":0}
    common_download_class=act2class[action](request)
    common_download_form=common_download_class.DownloadForm
    if request.method == "POST":
        uf = common_download_form(request.POST,request.FILES)
        if uf.is_valid():
            ret=common_download_class.download(uf)
        #  else:
            #  ret={"error":401}

        #  ret["time"]=int(round(time.time() * 1e3)/1e3)
            return ret
    else:
        uf = common_download_form()
        return render_to_response('common_upload.html',{'uf':uf})


def api(request):
    ret={"error":0}

    if request.method!='POST':
        ret["error"]=400
    post_data=json.loads(request.body)
    if ret["error"]==0 and not "action" in post_data:
        ret["error"]=402
        ret["field"]="action"

    request_action=post_data["action"]
    print request_action
    request_action_func_list={
        "user_register":user.register,
        "user_login":user.login,
        "user_logout":user.logout,
        "user_info":user.info,
        "user_edit_profile":user.edit_profile,
        "other_user_info":user.other_user_info,
        "my_card_list":user.my_card_list,

        "qr_query":qrcode.qr_query,

        "card_edit_query":card.card_edit_query,
        "card_edit":card.card_edit,
        "card_delete":card.card_ban,
        "card_restore":card.card_restore,
        "card_create":card.card_create,
        "card_query":card.card_query,
        "card_create_query":card.card_create_query,

        "res_query":res_query,
        "news_query":news.news_query,

    }
    if ret["error"]==0 and not request_action in request_action_func_list.keys():
        ret["error"]=404

    if ret["error"]==0:
        ret=request_action_func_list[request_action](request,post_data,ret)

    ret["time"]=int(round(time.time() * 1e3)/1e3)
    return HttpResponse(json.dumps(ret), content_type="application/json")

