from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.contrib import auth

from .models import *
import re
import json

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

    return HttpResponse(json.dumps(res))

def login(request):
    res={'error':-1}
    if (request.method=='POST'):
        res['error']=0
        if request.user.is_authenticated():
            res['error']=1

        req = json.loads(request.body)

        user = auth.authenticate(username=req['email'], password=req['password'])

        if user is not None and user.is_active:
            auth.login(request, user)
        else:
            res['error']=1
    return HttpResponse(json.dumps(res))



