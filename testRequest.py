#!/usr/bin/env python
#coding=utf-8

# @file testRequest.py
# @brief testRequest
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13

import sys
import requests
import json
import datetime
import time

reload(sys)
sys.setdefaultencoding("utf-8")
def testRequest():
    """Register"""
    #  reg={"email":"test001@126.com","pwd":"test001"}
    #  reg={"action":"user_register","account":reg}
    #  data=json.dumps(reg)
    #  r = requests.post("http://127.0.0.1:8000/api/courtesy",data)
    #  print r.text
    #  _cookies = r.cookies
    """Login"""
    reg={"email":"test001@126.com","pwd":"test001"}
    reg={"action":"user_login","account":reg}
    data=json.dumps(reg)
    r = requests.post("http://127.0.0.1:8000/api/courtesy",data)
    print r.text
    _cookies = r.cookies
    """Info"""
    #  reg={"action":"user_info","email":"test001@126.com"}
    #  data=json.dumps(reg)
    #  r = requests.post("http://127.0.0.1:8000/api/courtesy",data,cookies=_cookies)
    #  print r.text
    """Logout"""
    #  reg={"action":"user_logout"}
    #  data=json.dumps(reg)
    #  print r.text
    #  r = requests.post("http://127.0.0.1:80/api/courtesy",data,cookies=_cookies)
    #  _cookies = r.cookies
    #  print r.text

    """ news query """
    reg={"action":"news_query","s_date":"2016-03-31"}
    data=json.dumps(reg)
    print data
    r = requests.post("http://127.0.0.1:8000/api/courtesy",data,cookies=_cookies)
    print r.text

    """qr_query"""
    #  reg={"action":"qr_query","qr_id":"da3ac95ccd0c44e7e080b911bf57ce6c"}
    #  data=json.dumps(reg)
    #  print data
    #  r = requests.post("http://127.0.0.1:8000/api/courtesy",data,cookies=_cookies)
    #  print r.text

    """card_create"""
    #  reg={
        #  "action":"card_create",
        #  "qr_id":"c1f3f1106dd37d7538dd0a7946ccc025",
        #  "card_info":{
            #  "local_template":"you will do it :)",
            #  "is_public":True,
            #  "visible_at":time.mktime( datetime.datetime(1999,2,2).timetuple() ),
            #  "is_editable":True,
        #  }
    #  }
    #  data=json.dumps(reg)
    #  print data
    #  r = requests.post("http://127.0.0.1:8000/api/courtesy",data,cookies=_cookies)
    #  print r.text

    """card_query"""
    #  reg={"action":"card_query","token":"9d27cae6567cb2bb4cd5c3cd74854e42"}
    #  data=json.dumps(reg)
    #  print data
    #  r = requests.post("http://127.0.0.1:8000/api/courtesy",data,cookies=_cookies)
    #  print r.text

    """card_edit"""

    #  reg={
        #  "action":"card_edit",
        #  "token":"9d27cae6567cb2bb4cd5c3cd74854e42",
        #  "card_info":{
            #  "local_template":"you will do it :)",
            #  "is_public":True,
            #  "visible_at":time.time()+1000000,
            #  "is_editable":True,
        #  }
    #  }
    #  data=json.dumps(reg)
    #  print data
    #  r = requests.post("http://127.0.0.1:8000/api/courtesy",data,cookies=_cookies)
    #  print r.text


    #  reg={"action":"user_edit_profile",
        #  "profile":
            #  {"nick":"mike",
                #  "birthday":"1955-5-5",
                #  "gender":2,
                #  "province":"jiangsu",
                #  "city":"nanjing",
                #  "constellation":"notknow",
                #  "mobile":"8888"

            #  }
    #  }
    #  data=json.dumps(reg)
    #  r = requests.post("http://127.0.0.1:80/api/courtesy",data,cookies=_cookies)

    #  reg={"action":"account_info"}
    #  data=json.dumps(reg)
    #  r = requests.post("http://127.0.0.1:80/api/courtesy",data,cookies=_cookies)
    #  print r.text

    """res_query"""
    #  reg={"action":"res_query","hash":"3120c808d57e9818589b644ae2b6cb956e65f169b1972fa6de745da298a239d7"}
    #  data=json.dumps(reg)
    #  print data
    #  r = requests.post("http://127.0.0.1:8000/api/courtesy",data,cookies=_cookies)
    #  print r.text

if __name__ == '__main__':
    testRequest()
    raw_input()

