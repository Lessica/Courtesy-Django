#!/usr/bin/env python
#coding=utf-8

# @file user.py
# @brief user
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13
from django.contrib import auth
from django.core.exceptions import *
from django.db import IntegrityError

from models.account import *
from commonupload import *

def login(request,post_data,ret):
    #TODO:is logined
    #  if request.user.is_authenticated():
        #  ret['error']=408
        #  return ret
    try:
        req = post_data["account"]

        user = auth.authenticate(username=req['email'], password=req['pwd'])
        if user is None:
            ret['error']=406
        if ret['error']==0 and not user.is_active:
            ret['error']=407
        else:
            auth.login(request, user)
        #  um=UserModel.objects.get(user_ptr_id=request.user.id)
        #  um.last_login=timezone.now
        #  um.save()

    except KeyError as e:
        ret['error']=401
        ret["field"]=str(e)[1:-1]
    except AttributeError as e:
        if ret['error']!=406:
            ret['error']=406
            ret["field"]=str(e)[1:-1]
        #  ret['user_model']=UserModel.objects.get(user_ptr_id=user.id).toDict()
    #  return ret
    return ret

def register(request,post_data,ret):
    req=post_data["account"]
    try:
        user = UserModel.objects.create_user(
                                         username=req['email'],
                                         email=req['email'],
                                         )
        user.set_password(req['pwd'])
        user.nick=req["email"].split("@")[0]
        user.save()

        user = auth.authenticate(username=req['email'], password=req['pwd'])
        auth.login(request, user)
    except IntegrityError as e:
        ret['error']=405
        ret['field']=str(e).replace("username","email").split(" ")[1]
    #  except Exception:
        #  ret['error']=404


    return ret

def logout(request,post_data,ret):
    if not request.user.is_authenticated():
        ret["error"]=403
    else:
        try:
            auth.logout(request)
        except Exception:
            ret['error']=404

    return ret

def info(request,post_data,ret):
    if not request.user.is_authenticated():
        ret["error"]=403
        return ret
    if post_data.has_key("user_id"):
        user=UserModel.objects.get(user_ptr_id=post_data["user_id"])
    elif post_data.has_key("user_email"):
        user=UserModel.objects.get(email=post_data["user_email"])
    else:
        user=UserModel.objects.get(user_ptr_id=request.user.id)
    ret["account_info"]=user.toDict()
    ret["account_info"]["has_profile"] = True;
    return ret

def edit_profile(request,post_data,ret):
    try:
        if not request.user.is_authenticated():
            ret["error"]=403
        else:
            profile=post_data["profile"]
            user_model=UserModel.objects.get(user_ptr_id=request.user.id)
            user_model.nick=profile["nick"]
            #TODO:
            #  user_model.avatar=profile["avatar"]
            user_model.mobile=profile["mobile"]
            user_model.birthday=profile["birthday"]
            user_model.gender=profile["gender"]
            user_model.detailed_info=profile["introduction"]
            user_model.province=profile["province"]
            user_model.city=profile["city"]
            user_model.area=profile["area"]
            #  user_model.constellation=profile["constellation"]
            user_model.save()

    except KeyError as e:
        ret['error']=401
        ret["field"]=str(e)[1:-1]

    return ret

# TODO:
def password_change():
    res={'error':-1}
    if (request.method=='POST'):
        res['error']=0
        if not request.user.is_authenticated():
            res['error']=0
        else:
            request.user.set_password()

    return HttpResponse(json.dumps(res), content_type="application/json")

class UserAvatarUpload(CommonUpload):

    class UploadForm(forms.Form):
        avatar=forms.ImageField(required=True)

    def upload(self,uf):
        [id_md5,server_path,kind]=handle_uploaded_file(self.request.FILES['avatar'],str(time.time()),"avatar")
        url_path=server_path[7:]
        img=Image.open(server_path)
        res=CommonResourceModel(id_md5=id_md5)
        res.save()

        um=UserModel.objects.get(user_ptr_id=self.request.user.id)
        um.avatar=res
        um.save()
        self.ret["id"]=id_md5

        for size in [300,150,60]:
            img.thumbnail((size,size),Image.ANTIALIAS)
            save_to_path=server_path[:-4]+"_"+str(size)+".png"
            res=CommonResourceModel(id_md5=id_md5+"_"+str(size))
            res.save()
            #  self.ret[str(size)+"px"]={"id_md5":id_md5+".png"}
            img.save(save_to_path,"png")


class UserBannerUpload(CommonUpload):

    class UploadForm(forms.Form):
        banner=forms.ImageField(required=True)

    def upload(self,uf):
        [id_md5,server_path,kind]=handle_uploaded_file(self.request.FILES['banner'],str(time.time()),"banner")
        url_path=server_path[7:]
        img=Image.open(server_path)
        res=CommonResourceModel(id_md5=id_md5)
        res.save()

        um=UserModel.objects.get(user_ptr_id=self.request.user.id)
        um.banner=res
        um.save()
        self.ret["id"]=id_md5

        size=1200
        img.thumbnail((size,size),Image.ANTIALIAS)
        save_to_path=server_path[:-4]+"_"+str(size)+".jpg"
        res=CommonResourceModel(id_md5=id_md5+"_"+str(size)+".jpg")
        res.save()
        #  self.ret[str(size)+"px"]={"id_md5":id_md5+".png"}
        img.save(save_to_path,"jpg")
