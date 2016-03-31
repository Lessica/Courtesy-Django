#!/usr/bin/env python
#coding=utf-8

# @file qrcode.py
# @brief qrcode
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13

from django.core.exceptions import *
from django.db import IntegrityError
from django import forms
from django.http import HttpResponse

from models.qr import *
from models.account import *
from commonupload import *

import hashlib
import datetime
import time
import StringIO
from os.path import join


def qr_query(request,post_data,ret):
    qr_id=post_data["qr_id"]
    try:
        qr_model=QRCodeModel.objects.get(unique_id=qr_id)
    except ( ValueError,ObjectDoesNotExist ):
        ret["error"]=423
        return ret
    ret["qr_info"]=qr_model.toDict()
    qr_model.scan_count=qr_model.scan_count+1
    qr_model.save()

    return ret


class QRArriseDownload(object):
    def __init__(self,request):
        self.request=request

    class DownloadForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super(type(self),self).__init__(*args, **kwargs)
            choice=[]
            QRStyles=QRStyleModel.objects.all()
            for QRStyle in QRStyles:
                choice.append( (QRStyle.name,QRStyle.name) )

            self.fields["qr_style"] = forms.ChoiceField(choices=choice)
            self.fields["channel"]=forms.CharField(required=True)
            self.fields["num"]=forms.IntegerField(required=True)

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


        path=join("qr_gift","static","qrlist")
        qr_context_path=join(path,"qrlist.txt" )
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
            fpath = join("qr_gift","static","qr_template","border",filename)
            zf.write(fpath, "border.png")
        if qr_style_model.style_center_binary:
            filename = qr_style_model.style_center_binary.id_md5
            fpath = join("qr_gift","static","qr_template","center",qr_style_model.style_border_binary.id_md5+".png")
            zf.write(fpath, "center.png")

        filename = qr_style_model.style_script.id_md5
        fpath = join("qr_gift","static","qr_template","script",qr_style_model.style_script.id_md5+".py")
        zf.write(fpath, "script.py")
        zf.write(qr_context_path, "list.txt")
        zf.close()
        resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename={0}.zip'.format(qr_style_name)
        os.remove(qr_context_path)
        return resp


class QRStyleUpload(CommonUpload):
    #  def __init__(self,request,ret):
        #  self.request=request
        #  self.ret=ret
    class UploadForm(forms.Form):
        name = forms.CharField(required=True)

        style_border_binary=forms.FileField(required=False)
        style_center_binary=forms.FileField(required=False)
        style_script=forms.FileField(required=True)
    def upload(self,uf):
        name = uf.cleaned_data['name']
        #  try:
        model=QRStyleModel(name=name)
        sysarg=[]
        if self.request.FILES.has_key('style_border_binary'):
            file_id,file_path,kind=handle_uploaded_file(self.request.FILES['style_border_binary'],name,join("qr_template","border"))
            res1=CommonResourceModel(id_md5=file_id,kind=kind)
            res1.save()
            model.style_border_binary=res1
            sysarg.append(file_id)

        if self.request.FILES.has_key('style_center_binary'):
            file_id,file_path,kind=handle_uploaded_file(self.request.FILES['style_center_binary'],name,join("qr_template","center"))
            res2=CommonResourceModel(id_md5=file_id,kind=kind)
            res2.save()
            model.style_center_binary=res2
            sysarg.append(file_id)

        if self.request.FILES.has_key('style_script'):
            file_id,file_path,kind=handle_uploaded_file(self.request.FILES['style_script'],name,join("qr_template","script"))
            res3=CommonResourceModel(id_md5=file_id,kind=kind)
            res3.save()
            model.style_script=res3
            sysarg.append(file_id)


        model.save()

        self.ret["file_id"]=sysarg
        #  except Exception,e:
            #  self.ret["error"]=str(e)
