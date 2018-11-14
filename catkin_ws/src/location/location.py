#!/usr/bin/env python

import cv2
import Tkinter as tk
from Tkinter import *
from PIL import Image
from PIL import ImageTk

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
# from mercator import *
import re
import imp
mapping_man = imp.load_source('Mapping', '../movement/mapping.py')


OFFICE_SVG_PATH = '../navigation/mybot_navigation/maps/ufficio.pgm'
FILE_OFFICE_PATH = '../navigation/mybot_navigation/maps/ufficio.yaml'

# PIXEL = 37.7952755906

CONST_RESIZE = 5
MAP_SIZE = 50

# cdict1 = {'red':   ((0.0, 0.0, 0.0),
#                    (0.5, 0.0, 0.1),
#                    (1.0, 1.0, 1.0)),

#          'green': ((0.0, 0.0, 0.0),
#                    (1.0, 0.0, 0.0)),

#          'blue':  ((0.0, 0.0, 1.0),
#                    (0.5, 0.1, 0.0),
#                    (1.0, 0.0, 0.0))
#         }


class GUI_Manager:
	def __init__(self):
		#Get resolution value
		self.resolution_value = self.get_resolution()
		print(self.resolution_value)
		
		#Create APs list
		self.map_manager = mapping_man.Mapping()
		self.AP = self.map_manager.getAPs()
		self.AP_enabled = []

		#Set up GUI
		self.window = tk.Tk()  #Makes main window
		self.window.wm_title("Mapping Tino")
		self.window.config(background="#cdcdcd")
		
		print(self.window.winfo_x(), self.window.winfo_y())
		print(self.window.geometry())
		#Graphics window
		self.imageFrame = tk.Frame(self.window, width=600, height=500)
		self.imageFrame.grid(row=0, column=0, padx=10, pady=10)

		self.display1 = tk.Label(self.imageFrame,borderwidth = 0, highlightthickness = 0)
		self.display1.grid(row=0, column=0) #, padx=10, pady=2)  #Display 1
		self.display2 = tk.Frame(self.window, width = 350, height = 100)
		self.display2.config(background="#cdcdcd")
		self.display2.grid(row=0, column=1,sticky="N", padx=20, pady=10) #Display 2

		self.list_color = [["red","violet"],["blue","green"],["orange","black"]]
		self.norm = matplotlib.colors.Normalize(vmin=-90, vmax=-20)
		self.color_dict = {}
		i = 0
		col = 0
		ap_cbs = dict()
		for name in self.AP:
			ap_cbs[name] = tk.Checkbutton(self.display2, text=name, onvalue=True, offvalue=False)
			ap_cbs[name].config(background="#cdcdcd", borderwidth = 0, highlightthickness = 0)
			ap_cbs[name].var = tk.BooleanVar()
			ap_cbs[name]['variable'] = ap_cbs[name].var
			ap_cbs[name]['command'] = lambda w=ap_cbs[name]: self.upon_select(w)
			
			ap_cbs[name].grid(row=i, sticky=W)
			ap_cbs[name].config(fg=self.list_color[col][0])
			i = i+1
			self.color_dict[name] = col
			col = col+1
			if col >= len(self.list_color):
				col = 0

		# read image into matrix.
		self.map_image = cv2.imread(OFFICE_SVG_PATH)

	def upon_select(self, widget):
	    print("{}'s value is {}.".format(widget['text'], widget.var.get()))
	    print(self.AP[widget['text']])
	    #cv2.circle(self.resized_image,(20,20), 5, (0,0,255), -1)
	    if widget.var.get() == True:
			self.AP_enabled.append(widget['text'])
			self.draw_circle(widget['text'])
	    else:
			self.clear_label_image()
			self.AP_enabled.remove(widget['text'])
			self.image_to_color = self.resized_image.copy()
			for i in self.AP_enabled:
				self.draw_circle(i)
				print(i)
			self.show_frame(self.image_to_color)

	def draw_circle(self, name_ap):
	    print("DRAW ", name_ap)
	    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", self.list_color[self.color_dict[name_ap]])
	    for key, value in self.map_manager.createMappingAP(self.AP[name_ap]).items():
			print(key, value, cmap(self.norm(value))[:3])
			color = cmap(self.norm(value))[:3]
			self.clear_label_image()
			# print(int(key[0]/self.resolution_value)+(self.w_res/2), int(key[1]/self.resolution_value)+(self.h_res/2))
			print("X:",((self.w_res/2)-int(key[0]/self.resolution_value)))
			x = (self.w_res/2)+(int(key[0]/self.resolution_value)*CONST_RESIZE)
			y = (self.h_res/2)-(int(key[1]/self.resolution_value)*CONST_RESIZE)
			cv2.circle(self.image_to_color, (x,y), 4, (color[2]*255,color[1]*255,color[0]*255), -1)
			# circle(image, (cx, cy), 20, (0,0,255), -1)
			#print(color[0]*255,color[1]*255,color[2]*255)
			#check http://corecoding.com/utilities/rgb-or-hex-to-float.php
			self.show_frame(self.image_to_color)

	def get_info_image(self):
		# get image properties.
		self.h,self.w,self.bpp = np.shape(self.map_image)
		# print image properties.
		print "width: " + str(self.w)
		print "height: " + str(self.h)
		print "bpp: " + str(self.bpp)

	def resize_image(self):
		# resized_image = cv2.resize(m, (w/CONST_RESIZE,h/CONST_RESIZE))
		center_x = self.w/2
		center_y = self.h/2
		# cv2.circle(self.map_image, (int(center_x+0/self.resolution_value),
		# 	int(center_y-0/self.resolution_value)), 4/CONST_RESIZE, (0,0,255), -1)
		# print((-102.445/self.resolution_value)/CONST_RESIZE)

		map_center = self.map_image[center_x-MAP_SIZE:center_x+MAP_SIZE, center_y-MAP_SIZE:center_y+MAP_SIZE, :]
		#print("SHAPE",map_center.shape[0],map_center.shape[1]) #100,100
		self.resized_image = cv2.resize(map_center, (map_center.shape[0]*CONST_RESIZE,map_center.shape[1]*CONST_RESIZE),
		 interpolation = cv2.INTER_AREA)
		self.w_res = map_center.shape[0]*CONST_RESIZE
		self.h_res = map_center.shape[1]*CONST_RESIZE
		self.image_to_color = self.resized_image.copy()
		print("RES ",self.w_res, self.h_res) #500,500
		

	def find_rgb(self, imagename, r_query, g_query, b_query):
		img = Image.open(imagename)
		rgb = img.convert('RGB')
		for x in range(img.size[0]):
			for y in range(img.size[1]):
				r, g, b, = rgb.getpixel((x, y))
				if r == r_query and g == g_query and b == b_query:
					return (x,y)


	def show_frame(self, image):
		cv2image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
		img = Image.fromarray(cv2image)
		imgtk = ImageTk.PhotoImage(image=img)
		self.display1.imgtk = imgtk #Shows frame for display 1
		self.display1.configure(image=imgtk)
		# window.after(10, show_frame) 
	def clear_label_image(self):
	    self.display1.config(image='')

	def update(self):
		self.show_frame(self.resized_image)
		self.window.mainloop()  #Starts GUI

	def get_resolution(self):
		pattern = re.compile("resolution")
		for _, line in enumerate(open(FILE_OFFICE_PATH)):
			for _ in re.finditer(pattern, line):
				return float(line.split(":")[1][:-1])

if __name__ == "__main__":
	gui_manager = GUI_Manager()
	gui_manager.get_info_image()
	gui_manager.resize_image()

	gui_manager.update()


	
	




