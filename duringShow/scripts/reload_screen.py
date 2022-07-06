import logging
# from waveshare_epd import epd5in83_V2
import time
from PIL import Image,ImageDraw,ImageFont, ImageOps
import traceback
import sys
import os
import numpy
# import pkg_resources
# pkg_resources.require("numpy==`1.21.2")
from blend_modes import difference
from random import randint

#https://pypi.org/project/blend-modes/

logging.basicConfig(level=logging.DEBUG)

def reloading(dir_path, msg):
    libdir = os.path.join(dir_path, 'lib')
    if os.path.exists(libdir):
        sys.path.append(libdir)
    from waveshare_epd import epd5in83_V2
    try:
        epd = epd5in83_V2.EPD()
        logging.info("init and Clear")
        epd.init()
        # epd.Clear()
        
        # font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        # font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        
        logging.info("Read file")
        # if msg > 2 and msg < 5:
        image1 = Image.open(os.path.join(dir_path, 'output', '1', str(msg-1)+'.jpg'))
        image2 = Image.open(os.path.join(dir_path, 'output', '2', str(msg-1)+'.jpg'))
        image3 = Image.open(os.path.join(dir_path, 'output', '3', str(msg-1)+'.jpg'))
        # elif msg>4:
            # Himage = Image.open(os.path.join(dir_path, 'prepared_diff', str(file_number)+'.jpg'))

        # fullImage = Image.open(os.path.join(dir_path, 'stitched', str(msg)+'.jpg'))

        epd.display(epd.getbuffer(image1))
        time.sleep(2)
        epd.display(epd.getbuffer(image3))
        time.sleep(2)
        epd.display(epd.getbuffer(image2))
        time.sleep(2)
        
        logging.info("Clear...")
        # aepd.Clear()
        
        logging.info("Goto Sleep...")
        epd.sleep()
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd5in83_V2.epdconfig.module_exit()
        exit()