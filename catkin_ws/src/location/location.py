#!/usr/bin/python
import cv2
from Tkinter import *
from PIL import Image
from PIL import ImageTk

import numpy as np
from mercator import *


OFFICE_SVG_PATH = '../navigation/mybot_navigation/maps/ufficio.pgm'
# PIXEL = 37.7952755906

CONST_RESIZE = 5
MAP_SIZE = 50

def find_rgb(imagename, r_query, g_query, b_query):
    img = Image.open(imagename)
    rgb = img.convert('RGB')
    for x in range(img.size[0]):
       for y in range(img.size[1]):
           r, g, b, = rgb.getpixel((x, y))
           if r == r_query and g == g_query and b == b_query:
               return (x,y)

if __name__ == "__main__":
	# read image into matrix.
	m = cv2.imread(OFFICE_SVG_PATH)
	 
	# get image properties.
	h,w,bpp = np.shape(m)
	 
	# print image properties.
	print "width: " + str(w)
	print "height: " + str(h)
	print "bpp: " + str(bpp)

	# resized_image = cv2.resize(m, (w/CONST_RESIZE,h/CONST_RESIZE))
	center_x = w/2
	center_y = h/2
	map_center = m[center_y-MAP_SIZE:center_y+MAP_SIZE, center_x-MAP_SIZE:center_x+MAP_SIZE, :]

	resized_image = cv2.resize(map_center, (map_center.shape[0]*CONST_RESIZE,map_center.shape[1]*CONST_RESIZE),
	 interpolation = cv2.INTER_AREA)

	cv2.imshow('matrix', resized_image)
	cv2.waitKey(0)





