#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
import logging
from signal import pause

# Raspberry Pi specific modules
from waveshare_epd import epd2in7b
from PIL import Image,ImageDraw,ImageFont
from gpiozero import Button

pic_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
lib_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(lib_dir):
    sys.path.append(lib_dir)

logging.basicConfig(level=logging.DEBUG)


def main():
    # 1. Draw the display with temp 70º
    th = Thermostat(70)

    # the corresponding pins from top to bottom are 5, 6, 13, 19
    # 2. If Up Button, set temp and redraw display
    up_btn = Button(5)
    up_btn.when_pressed = th.up

    # 3. If Down Button, set temp and redraw display
    down_btn = Button(6)
    down_btn.when_pressed = th.down

    # 4. Wait forever for buttons to be pressed
    pause()


class Thermostat:
    def __init__(self, target_temp=None, current_temp=None):
        self.target_temp = target_temp
        self.current_temp = current_temp
        self._draw()

    def up(self):
        self._set_target(self.target_temp + 1)

    def down(self):
        self._set_target(self.target_temp - 1)

    def _set_target(self, new_temp):
        logging.info('Target Temp: ' + str(new_temp))
        self.target_temp = new_temp
        self._draw()

    def _draw(self):
        epd = epd2in7b.EPD()
        epd.init()
        epd.Clear()

        font24 = ImageFont.truetype(os.path.join(pic_dir, 'Font.ttc'), 24)
        # font18 = ImageFont.truetype(os.path.join(pic_dir, 'Font.ttc'), 18)

        # Horizontal orientation size: 298x126
        h_black_img = Image.new('1', (epd.height, epd.width), 255)
        h_red_img = Image.new('1', (epd.height, epd.width), 255)

        draw_black = ImageDraw.Draw(h_black_img)
        draw_red = ImageDraw.Draw(h_red_img)

        draw_black.text((10, 0), 'Hello World', font=font24, fill=0)
        draw_black.text((10, 20), 'Temp: ' + str(self.target_temp), font=font24, fill=0)
        draw_black.line((20, 50, 70, 100), fill=0)
        draw_black.line((70, 50, 20, 100), fill=0)
        draw_black.rectangle((20, 50, 70, 100), outline=0)

        draw_red.line((165, 50, 165, 100), fill=0)
        draw_red.line((140, 75, 190, 75), fill=0)
        draw_red.arc((140, 50, 190, 100), 0, 360, fill=0)
        draw_red.rectangle((80, 50, 130, 100), fill=0)
        draw_red.chord((200, 50, 250, 100), 0, 360, fill=0)
        epd.display(epd.getbuffer(h_black_img), epd.getbuffer(h_red_img))


if __name__ == '__main__':
    main()
