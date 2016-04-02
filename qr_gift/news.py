#!/usr/bin/env python
#coding=utf-8

# @file news.py
# @brief news
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13

from models.daliynews import *
from commonupload import *
from os.path import join
import datetime
import time

def news_query(request,post_data,ret):
    date_str=post_data["s_date"]
    md_news=DaliyNewsModel.objects.get(date_str=date_str)
    ret["news"]=md_news.toDict()
    return ret

class DaliyNewsUpload(CommonUpload):
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
            self.fields["fdate"]=forms.DateField(initial=datetime.date.today,widget=forms.SelectDateWidget(years=[y for y in range(2000,2050)]))
            self.fields["fstring"]=forms.CharField(widget=forms.Textarea)
            self.fields["fid"] = forms.ChoiceField(choices=choice)

    def upload(self,uf):
        date_str=uf.cleaned_data['fdate']
        model=DaliyNewsModel.objects.get_or_create(date_str=date_str)[0]
        model.string=uf.cleaned_data['fstring']

        file_id,file_path,kind=handle_uploaded_file(self.request.FILES['image_res'],str(time.time()),join("news","image"))
        res1=CommonResourceModel(id_md5=file_id,kind=kind)
        res1.save()
        model.image=res1

        if self.request.FILES.has_key('voice_res'):
            file_id,file_path,kind=handle_uploaded_file(self.request.FILES['voice_res'],str(time.time()),join("news","voice"))
            res2=CommonResourceModel(id_md5=file_id,kind=kind)
            res2.save()
            model.voice=res2

        if self.request.FILES.has_key('video_res'):
            file_id,file_path,kind=handle_uploaded_file(self.request.FILES['video_res'],str(time.time()),join("news","video"))
            res3=CommonResourceModel(id_md5=file_id,kind=kind)
            res3.save()
            model.video=res3

        model.style=DaliyNewsStyleModel.objects.get(id=uf.cleaned_data['fid'])
        model.save()
