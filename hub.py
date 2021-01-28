#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7b
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from gpiozero import Button

logging.basicConfig(level=logging.DEBUG)

def main():
    # the corresponding pins from top to bottom are 5, 6, 13, 19
    # from gpiozero import Button
    # btn = Button(5)
    # btn.when_pressed = handleBtnPress
    btn5 = Button(5)
    epd = epd2in7b.EPD()
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    HRedimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126

    drawblack = ImageDraw.Draw(HBlackimage)
    drawred = ImageDraw.Draw(HRedimage)

    drawblack.text((10, 0), 'Hello World', font = font24, fill = 0)
    drawblack.text((10, 20), 'Temp:', font = font24, fill = 0)
    drawblack.line((20, 50, 70, 100), fill = 0)
    drawblack.line((70, 50, 20, 100), fill = 0)
    drawblack.rectangle((20, 50, 70, 100), outline = 0)

    drawred.line((165, 50, 165, 100), fill = 0)
    drawred.line((140, 75, 190, 75), fill = 0)
    drawred.arc((140, 50, 190, 100), 0, 360, fill = 0)
    drawred.rectangle((80, 50, 130, 100), fill = 0)
    drawred.chord((200, 50, 250, 100), 0, 360, fill = 0)
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))



class Thermostat:
    def __init__(self, desired_temp=None, initial_temp=None):
        self.desired_temp = desired_temp
        self.current_temp = initial_temp


if __name__ == '__main__':
    main()

