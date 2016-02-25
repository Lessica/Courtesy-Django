from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.contrib import auth
from django import forms
import django.utils.timezone as timezone

from .models import *
import re
import json
import hashlib
from wsgiref.util import FileWrapper
from os.path import join as jn
import zipfile
import StringIO
import time
import Image

SITE_ADDR="http://10.1.0.2222:8000/"

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
        UserModel.objects.get(user_ptr_id=request.user.id).last_login_at=timezone.now
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
        #  user.nick=req['nick']
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
    else:
        ret["account_info"]=UserModel.objects.get(user_ptr_id=request.user.id).toDict()
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
            user_model.province=profile["province"]
            user_model.city=profile["city"]
            user_model.constellation=profile["constellation"]
            user_model.save()

    except KeyError as e:
        ret['error']=401
        ret["field"]=str(e)[1:-1]

    return ret

class UserAvatarUpload(object):
    def __init__(self,request,ret):
        self.request=request
        self.ret=ret
    class UploadForm(forms.Form):
        avatar=forms.ImageField(required=True)

    def upload(self):
        server_path=handle_uploaded_file(self.request.FILES['avatar'],str(time.time()),"avatar")
        url_path=server_path[7:]
        img=Image.open(server_path)
        if img.size[0]!=img.size[1]:
            self.ret["error"]=422
            os.remove(server_path)
        else:
            res=CommonResourceModel(origin_url=url_path)
            res.save()
            self.ret["origin"]={"url":url_path}
            for size in [300,150,60]:
                img.thumbnail((size,size),Image.ANTIALIAS)
                save_to_path=server_path[:-4]+"_"+str(size)+".png"
                res=CommonResourceModel(origin_url=save_to_path[7:])
                res.save()
                self.ret[str(size)+"px"]={"url":save_to_path[7:]}
                img.save(save_to_path,"png")

def handle_uploaded_file(file,md5_str,path):
    m2=hashlib.md5(file.name.encode("utf-8")+md5_str)
    file_type=file.name.split('.')[1]
    des_path=jn("qr_gift","static",path,m2.hexdigest()+"."+file_type)
    destination = open(des_path , 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    return des_path

def common_upload(request,action):
    if not request.user.is_authenticated():
        ret={"error":403}
        return HttpResponse(json.dumps(ret), content_type="application/json")

    act2class={
        "avatar":UserAvatarUpload,

    }
    ret={"error":0}
    common_upload_class=act2class[action](request,ret)
    common_upload_form=common_upload_class.UploadForm

    if request.method == "POST":
        uf = common_upload_form(request.POST,request.FILES)
        if uf.is_valid():
            common_upload_class.upload()
            ret=common_upload_class.ret
        else:
            ret={"error":401}
        return HttpResponse(json.dumps(ret), content_type="application/json")
    else:
        uf = common_upload_form()
        return render_to_response('common_upload.html',{'uf':uf})

def user_avatar_upload(request):
    ret={"error":0}
    if not request.user.is_authenticated():
        ret={"error":403}
    if request.method == "POST":
        uf = UserUploadForm(request.POST,request.FILES)
        if uf.is_valid():
            file_path=handle_uploaded_file(request.FILES['avatar'],str(time.time()),"avatar")
            file_path=file_path[7:]
            res=CommonResourceModel(origin_url=file_path)
            res.save()
            ret["res"]=res.toDict()
        else:
            ret={"error":403}
        return HttpResponse(json.dumps(ret), content_type="application/json")
    else:
        uf = UserUploadForm()
        return render_to_response('common_upload.html',{'uf':uf})

def password_change():
    res={'error':-1}
    if (request.method=='POST'):
        res['error']=0
        if not request.user.is_authenticated():
            res['error']=0
        else:
            request.user.set_password()

    return HttpResponse(json.dumps(res), content_type="application/json")

class UserForm(forms.Form):
    name = forms.CharField(required=True)

    style_border_binary=forms.FileField(required=False)
    style_center_binary=forms.FileField(required=False)
    style_script=forms.FileField(required=True)

def qr_style_upload(request):
    if not request.user.is_authenticated():
        return HttpResponse("need super user!")
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

def send_zipfile(request,filenames,zip_filename="test.zip"):
    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()
    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = jn( "qr_gift","static",fname )

        # Add file, at correct path
        zf.write(fpath, zip_path)
    # Must close zip for all contents to be written
    zf.close()
    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    return resp

class QR_Form(forms.Form):
    choice=[]
    QRStyles=QRStyleModel.objects.all()
    for QRStyle in QRStyles:
        choice.append( (QRStyle.name,QRStyle.name) )

    qr_style = forms.ChoiceField(choices=choice)
    channel=forms.CharField(required=True)
    num=forms.IntegerField(required=True)
def qr_arrise(request):
    if not request.user.is_authenticated():
        return HttpResponse("need super user!")
    if request.method == "POST":
        uf = QR_Form(request.POST)
        if uf.is_valid():
            qr_style_name = uf.cleaned_data['qr_style']
            qr_channel = uf.cleaned_data['channel']
            num = uf.cleaned_data['num']
            qr_style_model=QRStyleModel.objects.get(name=qr_style_name)

            qr_list=[]
            qr_content=[]
            for i in range(0,num):
                qr_id=hashlib.md5(str(time.time())+str(i)).hexdigest()
                qr_list.append(QRCodeModel(channel=qr_channel,style=qr_style_model,unique_id=qr_id))
                qr_content.append(SITE_ADDR+"qrcode/scan/?unique_id"+qr_id)

            QRCodeModel.objects.bulk_create(qr_list)

            qr_context_path=jn("qr_gift","static","qrlist","qrlist.txt" )
            qr_context=open(qr_context_path,"w")
            qr_context.write( "\n".join(qr_content) )
            qr_context.close()

            # Open StringIO to grab in-memory ZIP contents
            s = StringIO.StringIO()
            # The zip compressor
            zf = zipfile.ZipFile(s, "w")

            if qr_style_model.style_border_binary:
                fdir, fname = os.path.split(qr_style_model.style_border_binary.origin_url)
                fpath = "qr_gift"+qr_style_model.style_border_binary.origin_url
                zf.write(fpath, "border"+fname[-4:])
            if qr_style_model.style_center_binary:
                fdir, fname = os.path.split(qr_style_model.style_center_binary.origin_url)
                fpath = "qr_gift"+qr_style_model.style_center_binary.origin_url
                zf.write(fpath, "center"+fname[-4:])

            fdir, fname = os.path.split(qr_style_model.style_script.origin_url)
            fpath = "qr_gift"+qr_style_model.style_script.origin_url
            zf.write(fpath, "script.py")
            zf.write(qr_context_path, "list.txt")
            zf.close()
            resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
            resp['Content-Disposition'] = 'attachment; filename={0}.zip'.format(qr_style_name)
            os.remove(qr_context_path)
            return resp
    else:
        uf = QR_Form()
    return render_to_response('qr_arrise.html',{'uf':uf})


def api(request):
    time.sleep(3)
    ret={"error":0}

    if request.method!='POST':
        ret["error"]=400
    post_data=json.loads(request.body)
    if ret["error"]==0 and not "action" in post_data:
        ret["error"]=402
        ret["field"]="action"
    request_action=post_data["action"]
    request_action_func_list={
        "user_register":register,
        "user_login":login,
        "user_logout":logout,
        "user_info":user_info,
        "user_edit_profile":user_edit_profile
    }
    if ret["error"]==0 and not request_action in request_action_func_list.keys():
        ret["error"]=404

    if ret["error"]==0:
        ret=request_action_func_list[request_action](request,post_data,ret)

    ret["time"]=int(round(time.time() * 1e3)/1e3)
    return HttpResponse(json.dumps(ret), content_type="application/json")
