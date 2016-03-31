#!/usr/bin/env python
#coding=utf-8

# @file commonupload.py
# @brief commonupload
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13
from django import forms

import hashlib
import os
from os.path import join


def handle_uploaded_file(file,md5_str,path):
    m2=hashlib.md5(file.name.encode("utf-8")+md5_str)
    file_type=file.name.split('.')[1]
    path=join("qr_gift","static",path)
    file_path=join(path,m2.hexdigest()+"."+file_type)
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


class CommonUpload(object):
    def __init__(self,request,ret):
        self.request=request
        self.ret=ret

    class UploadForm(forms.Form):
        pass

    def upload(self,uf):
        pass

