from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.contrib import auth
from django import forms

from .models import *
import re
import json
import hashlib
from wsgiref.util import FileWrapper
from os.path import join as jn
import zipfile
import StringIO
import time

SITE_ADDR="http://10.1.0.2222:8000/"


def register(request):
    res={'error':-1}
    if (request.method=='POST'):
        req = json.loads(request.body)
        res={"error":0}
        try:
            user = UserModel.objects.create_user(
                                             username=req['email'],
                                             email=req['email'],
                                             )
            user.set_password(req['password'])
            user.nick=req['nick']
            user.save()
        except IntegrityError as e:
            res['error']=1

    return HttpResponse(json.dumps(res), content_type="application/json")

def login(request):
    res={'error':-1}
    if (request.method=='POST'):
        res['error']=0
        if request.user.is_authenticated():
            res['error']=1

        req = json.loads(request.body)

        user = auth.authenticate(username=req['email'], password=req['password'])

        if user is None:
            res['error']=2
        if not user.is_active:
            res['error']=3
        else:
            auth.login(request, user)
            res['user_model']=UserModel.objects.get(user_ptr_id=user.id).toDict()

    return HttpResponse(json.dumps(res), content_type="application/json")

def logout(request):
    res={'error':0}
    auth.logout(request)
    return HttpResponse(json.dumps(res), content_type="application/json")

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


def handle_uploaded_file(file,name,path):
    m2=hashlib.md5(name+file.name)
    type=file.name.split('.')[1]
    des_path=jn("qr_gift","static",path,m2.hexdigest()+"."+type)
    destination = open(des_path , 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    return des_path
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
