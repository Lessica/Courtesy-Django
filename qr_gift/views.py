from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.contrib import auth
from django import forms
from django.core.exceptions import *

from .models import *
import re
import json
import hashlib
from wsgiref.util import FileWrapper
from os.path import join as jn
import zipfile
import StringIO
import time
from PIL import Image
import datetime
import os

#######################################################
################## USER PART #######################
#######################################################

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

def user_info(request,post_data,ret):
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

def user_edit_profile(request,post_data,ret):
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

"""
QR_CODE PART
"""
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

"""
    news
"""

def news_query(request,post_data,ret):
    date_str=post_data["s_date"]
    md_news=DaliyNewsModel.objects.get(date_str=date_str)
    ret["news"]=md_news.toDict()
    return ret


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

def get_file_md5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()
def handle_uploaded_file(file,md5_str,path):
    m2=hashlib.md5(file.name.encode("utf-8")+md5_str)
    file_type=file.name.split('.')[1]
    path=jn("qr_gift","static",path)
    file_path=jn(path,m2.hexdigest()+"."+file_type)
    if not os.path.exists( path ):
        os.makedirs(path)
    destination = open(file_path , 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    return m2.hexdigest(),file_path,file_type
def file2sha256(filename):
    f = open(filename, 'rb')
    sh = hashlib.sha256()
    sh.update(f.read())
    f.close()
    return sh.hexdigest()


class UserAvatarUpload(object):
    def __init__(self,request,ret):
        self.request=request
        self.ret=ret
    class UploadForm(forms.Form):
        avatar=forms.ImageField(required=True)

    def upload(self,uf):
        [id_md5,server_path,kind]=handle_uploaded_file(self.request.FILES['avatar'],str(time.time()),"avatar")
        url_path=server_path[7:]
        img=Image.open(server_path)
        res=CommonResourceModel(id_md5=id_md5)
        res.save()
        self.ret["id"]=id_md5
        for size in [300,150,60]:
            img.thumbnail((size,size),Image.ANTIALIAS)
            save_to_path=server_path[:-4]+"_"+str(size)+".png"
            res=CommonResourceModel(id_md5=id_md5+"_"+str(size)+".png")
            res.save()
            #  self.ret[str(size)+"px"]={"id_md5":id_md5+".png"}
            img.save(save_to_path,"png")
            if size==300:
                um=UserModel.objects.get(user_ptr_id=self.request.user.id)
                um.avatar=res
                um.save()

class QRStyleUpload(object):
    def __init__(self,request,ret):
        self.request=request
        self.ret=ret
    class UploadForm(forms.Form):
        name = forms.CharField(required=True)

        style_border_binary=forms.FileField(required=False)
        style_center_binary=forms.FileField(required=False)
        style_script=forms.FileField(required=True)
    def upload(self,uf):
        name = uf.cleaned_data['name']
        try:
            model=QRStyleModel(name=name)
            sysarg=[]
            if self.request.FILES.has_key('style_border_binary'):
                file_id,file_path,kind=handle_uploaded_file(self.request.FILES['style_border_binary'],name,jn("qr_template","border"))
                res1=CommonResourceModel(id_md5=file_id,kind=kind)
                res1.save()
                model.style_border_binary=res1
                sysarg.append(file_id)

            if self.request.FILES.has_key('style_center_binary'):
                file_id,file_path,kind=handle_uploaded_file(self.request.FILES['style_center_binary'],name,jn("qr_template","center"))
                res2=CommonResourceModel(id_md5=file_id,kind=kind)
                res2.save()
                model.style_center_binary=res2
                sysarg.append(file_id)

            if self.request.FILES.has_key('style_script'):
                file_id,file_path,kind=handle_uploaded_file(self.request.FILES['style_script'],name,jn("qr_template","script"))
                res3=CommonResourceModel(id_md5=file_id,kind=kind)
                res3.save()
                model.style_script=res3
                sysarg.append(file_id)


            model.save()

            self.ret["file_id"]=sysarg
        except Exception,e:
            self.ret["error"]=e

class DaliyNewsUpload(object):
    def __init__(self,request,ret):
        self.request=request
        self.ret=ret
    class UploadForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super(type( self ),self).__init__(*args, **kwargs)

            choice=[]
            styles=DaliyNewsStyleModel.objects.all()
            for style in styles:
                choice.append( (style.id,style.style_name) )

            self.fields["image_res"]=forms.FileField(required=True)
            self.fields["voice_res"]=forms.FileField(required=False)
            self.fields["video_res"]=forms.FileField(required=False)
            #  self.fields["fdate"]=forms.CharField()
            self.fields["fdate"]=forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget(years=[y for y in range(2000,2050)]))
            self.fields["fstring"]=forms.CharField(widget=forms.Textarea)
            self.fields["fid"] = forms.ChoiceField(choices=choice)

    def upload(self,uf):
        date_str=uf.cleaned_data['fdate']
        model=DaliyNewsModel.objects.get_or_create(date_str=date_str)[0]
        model.string=uf.cleaned_data['fstring']

        file_id,file_path,kind=handle_uploaded_file(self.request.FILES['image_res'],str(time.time()),jn("news","image"))
        res1=CommonResourceModel(id_md5=file_id,kind=kind)
        res1.save()
        model.image=res1

        if self.request.FILES.has_key('voice_res'):
            file_id,file_path,kind=handle_uploaded_file(self.request.FILES['voice_res'],str(time.time()),jn("news","voice"))
            res2=CommonResourceModel(id_md5=file_id,kind=kind)
            res2.save()
            model.voice=res2

        if self.request.FILES.has_key('video_res'):
            file_id,file_path,kind=handle_uploaded_file(self.request.FILES['video_res'],str(time.time()),jn("news","video"))
            res3=CommonResourceModel(id_md5=file_id,kind=kind)
            res3.save()
            model.video=res3

        model.style=DaliyNewsStyleModel.objects.get(id=uf.cleaned_data['fid'])
        model.save()

class CardResourceUpload(object):
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

def common_upload(request,action):
    if not request.user.is_authenticated():
        ret={"error":403}
        return HttpResponse(json.dumps(ret), content_type="application/json")

    act2class={
        "avatar":UserAvatarUpload,
        "qr_style":QRStyleUpload,
        "card_res":CardResourceUpload,
        "news":DaliyNewsUpload,
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


class QRArriseDownloadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QRArriseDownloadForm,self).__init__(*args, **kwargs)
        choice=[]
        QRStyles=QRStyleModel.objects.all()
        for QRStyle in QRStyles:
            choice.append( (QRStyle.name,QRStyle.name) )

        self.fields["qr_style"] = forms.ChoiceField(choices=choice)
        self.fields["channel"]=forms.CharField(required=True)
        self.fields["num"]=forms.IntegerField(required=True)

class QRArriseDownload(object):
    def __init__(self,request):
        self.request=request
    def download(self,uf):
        qr_style_name = uf.cleaned_data['qr_style']
        qr_channel = uf.cleaned_data['channel']
        num = uf.cleaned_data['num']
        qr_style_model=QRStyleModel.objects.get(name=qr_style_name)

        qr_list=[]
        qr_content=[]
        for i in range(0,num):
            qr_id=hashlib.md5(str(time.time())+str(i)).hexdigest()
            qr_list.append(QRCodeModel(channel=qr_channel,style=qr_style_model,unique_id=qr_id))
            qr_content.append(qr_id)

        QRCodeModel.objects.bulk_create(qr_list)


        path=jn("qr_gift","static","qrlist")
        qr_context_path=jn(path,"qrlist.txt" )
        if not os.path.exists( path ):
            os.makedirs(path)
        qr_context=open(qr_context_path,"w")
        qr_context.write( "\n".join(qr_content) )
        qr_context.close()

        # Open StringIO to grab in-memory ZIP contents
        s = StringIO.StringIO()
        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        if qr_style_model.style_border_binary:
            filename = qr_style_model.style_border_binary.id_md5+".png"
            fpath = jn("qr_gift","static","qr_template","border",filename)
            zf.write(fpath, "border.png")
        if qr_style_model.style_center_binary:
            filename = qr_style_model.style_center_binary.id_md5
            fpath = jn("qr_gift","static","qr_template","center",qr_style_model.style_border_binary.id_md5+".png")
            zf.write(fpath, "center.png")

        filename = qr_style_model.style_script.id_md5
        fpath = jn("qr_gift","static","qr_template","script",qr_style_model.style_script.id_md5+".py")
        zf.write(fpath, "script.py")
        zf.write(qr_context_path, "list.txt")
        zf.close()
        resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename={0}.zip'.format(qr_style_name)
        os.remove(qr_context_path)
        return resp

def common_download(request,action):
    if not request.user.is_authenticated():
        ret={"error":403}
        return HttpResponse(json.dumps(ret), content_type="application/json")

    act2class={
        "qr_arrise":( QRArriseDownload,QRArriseDownloadForm ),
    }
    #  ret={"error":0}
    common_download_class=act2class[action][0](request)
    common_download_form=act2class[action][1]
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

def qr_arrise(request):
    if not request.user.is_authenticated():
        return HttpResponse("need super user!")
    if request.method == "POST":
        uf = QR_Form(request.POST)
        if uf.is_valid():
            pass
    else:
        uf = QR_Form()
    return render_to_response('qr_arrise.html',{'uf':uf})



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
        "user_register":register,
        "user_login":login,
        "user_logout":logout,
        "user_info":user_info,
        "user_edit_profile":user_edit_profile,
        "qr_query":qr_query,
        "card_edit":card_edit,
        "card_create":card_create,
        "card_query":card_query,
        "res_query":res_query,
        "news_query":news_query,
    }
    if ret["error"]==0 and not request_action in request_action_func_list.keys():
        ret["error"]=404

    if ret["error"]==0:
        ret=request_action_func_list[request_action](request,post_data,ret)

    ret["time"]=int(round(time.time() * 1e3)/1e3)
    return HttpResponse(json.dumps(ret), content_type="application/json")

def qr_style_upload(request):
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            name = uf.cleaned_data['name']
            try:
                model=QRStyleModel(name=name)
                sysarg=[]
                if request.FILES.has_key('style_border_binary'):
                    file_path=handle_uploaded_file(request.FILES['style_border_binary'],name,jn("qr_template","border"))
                    file_path=file_path[7:]
                    res1=CommonResourceModel(origin_url=file_path)
                    res1.save()
                    model.style_border_binary=res1
                    sysarg.append(file_path)

                if request.FILES.has_key('style_center_binary'):
                    file_path=handle_uploaded_file(request.FILES['style_center_binary'],name,jn("qr_template","center"))
                    file_path=file_path[7:]
                    res2=CommonResourceModel(origin_url=file_path)
                    res2.save()
                    model.style_center_binary=res2
                    sysarg.append(file_path)

                if request.FILES.has_key('style_script'):
                    file_path=handle_uploaded_file(request.FILES['style_script'],name,jn("qr_template","script"))
                    file_path=file_path[7:]
                    res3=CommonResourceModel(origin_url=file_path)
                    res3.save()
                    model.style_script=res3
                    sysarg.append(file_path)

                if request.FILES.has_key('Sytle_'):
                    file_path=handle_uploaded_file(request.FILES['style_script'],name,jn("qr_template","script"))
                    file_path=file_path[7:]
                    res3=CommonResourceModel(origin_url=file_path)
                    res3.save()
                    model.style_script=res3
                    sysarg.append(file_path)


                model.save(args)

                return HttpResponse(sysarg)
            except Exception,e:
                return HttpResponse(e)

    else:
        uf = UserForm()
    return render_to_response('qr_style_upload.html',{'uf':uf})

