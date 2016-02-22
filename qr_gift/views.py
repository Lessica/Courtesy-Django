from django.shortcuts import render
from django.http import HttpResponse

from .models import *
import re
import json

def register(request):
    setattr(request, '_dont_enforce_csrf_checks', True)
    if (request.method=='POST'):
        req = json.loads(request.body)
        un=re.match(".*@",req['email']).group()[:-1]

        user = UserModel.objects.create_user(
                                         username=un,
                                         email=req['email'],
                                         )
        user.nick=req['nick']
        user.set_password(req['password'])
        return HttpResponse(user)
