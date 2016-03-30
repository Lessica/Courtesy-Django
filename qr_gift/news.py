#!/usr/bin/env python
#coding=utf-8

# @file news.py
# @brief news
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13

from .models import daliynews

def news_query(request,post_data,ret):
    date_str=post_data["s_date"]
    md_news=DaliyNewsModel.objects.get(date_str=date_str)
    ret["news"]=md_news.toDict()
    return ret
