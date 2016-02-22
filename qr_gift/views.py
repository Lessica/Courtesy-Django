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
from os.path import join as jn

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
    des_path=jn (jn( jn("qr_gift","static"),path ) ,m2.hexdigest()+"."+type)
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
            #  try:
            name = uf.cleaned_data['name']
            model=QRStyleModel(name=name)
            if request.FILES.has_key('style_border_binary'):
                file_path=handle_uploaded_file(request.FILES['style_border_binary'],name,jn("qr_template","border"))
                file_path=file_path[7:]
                res1=CommonResourceModel(origin_url=file_path)
                res1.save()
                model.style_border_binary=res1

            if request.FILES.has_key('style_center_binary'):
                file_path=handle_uploaded_file(request.FILES['style_center_binary'],name,jn("qr_template","center"))
                file_path=file_path[7:]
                res2=CommonResourceModel(origin_url=file_path)
                res2.save()
                model.style_center_binary=res2

            if request.FILES.has_key('style_script'):
                file_path=handle_uploaded_file(request.FILES['style_script'],name,jn("qr_template","script"))
                file_path=file_path[7:]
                res3=CommonResourceModel(origin_url=file_path)
                res3.save()
                model.style_script=res3
            model.save()

            return HttpResponse("success")
            #  except Exception,e:
                #  return HttpResponse(e)

    else:
        uf = UserForm()
    return render_to_response('qr_style_upload.html',{'uf':uf})
