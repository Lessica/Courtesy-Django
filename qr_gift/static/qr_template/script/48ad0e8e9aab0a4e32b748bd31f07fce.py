#!/usr/bin/env python
#coding=utf-8

# @file script.py
# @brief script
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2016-02-13

import sys
import Image

reload(sys)
sys.setdefaultencoding("utf-8")
def script(image_name,border_name):
    im=Image.open(image_name)
    im_size=im.size
    border=Image.open(border_name)
    border_size=border.size
    image = Image.new('RGB', (im_size[0], im_size[1]+border_size[1]), (255, 255, 255))
    x=y=0
    image.paste(im,(x,y))
    image.paste(border,(x,y+im_size[1]))
    image.save("fin.png")

if __name__ == '__main__':
    script(sys.argv[1],sys.argv[2])
