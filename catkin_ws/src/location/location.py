#!/usr/bin/env python

import cv2
from sys import version_info
if version_info.major == 2: # Python 2.x
	import Tkinter as tk
	from Tkinter import *
elif version_info.major == 3: # Python 3.x
	import tkinter as tk
	from tkinter import *
from PIL import Image
from PIL import ImageTk

import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib import cm
# from colorspacious import cspace_converter
from collections import OrderedDict
# from mercator import *
import re,os
import imp
mapping_man = imp.load_source('Mapping', 'waypoint/mapping.py')


OFFICE_SVG_PATH = '../navigation/mybot_navigation/map_cubo/corridoio_all_good.pgm'
FILE_OFFICE_PATH = '../navigation/mybot_navigation/map_cubo/corridoio_all_good.yaml'
IMAGE_ICON = 'img/wifi_icon.png'
# PIXEL = 37.7952755906

CONST_RESIZE = 1
CONST_RESIZE_CIRCLE = 1
MAP_SIZE = 400
MIN_VALUE_FREQUENCY = -80
MAX_VALUE_FREQUENCY = -50

class GUI_Manager:
	def reverse_colourmap(self,cmap, name = 'my_cmap_r'):
		reverse = []
		k = []   

		for key in cmap._segmentdata:    
			k.append(key)
			channel = cmap._segmentdata[key]
			data = []

			for t in channel:                    
				data.append((1-t[0],t[2],t[1]))            
			reverse.append(sorted(data))    

		LinearL = dict(zip(k,reverse))
		my_cmap_r = mpl.colors.LinearSegmentedColormap(name, LinearL) 
		return my_cmap_r

	def __init__(self):
		#Get resolution value
		self.resolution_value = self.get_resolution()
		print(self.resolution_value)
		self.get_center()
		#Create APs list
		self.map_manager = mapping_man.Mapping()
		self.AP = self.map_manager.getAPs()
		self.AP_enabled = []
		self.mapping_AP = {}

		#Set up GUI
		self.window = tk.Tk()  #Makes main window
		self.window.wm_title("Mapping Tino")
		imgicon = PhotoImage(file=IMAGE_ICON)
		self.window.tk.call('wm','iconphoto', self.window._w, imgicon)
		self.window.config(background="#cdcdcd")
		
		#Graphics window
		self.imageFrame = tk.Frame(self.window, width=900, height=500)
		self.imageFrame.grid(row=0, column=0, padx=10, pady=10)

		self.display1 = tk.Label(self.imageFrame,borderwidth = 0, highlightthickness = 0)#, width=800, height=500)
		self.display1.grid(row=0, column=0) #, padx=10, pady=2)  #Display 1
		self.display2 = tk.Frame(self.window, width = 350, height = 100)
		self.display2.config(background="#cdcdcd")
		self.display2.grid(row=0, column=1,sticky="N", padx=50, pady=10) #Display 2

		self.tuple_mapping = dict()
		self.cmaps = OrderedDict()

		self.cmaps['Sequential'] = [
			'Oranges', 'Purples', 'Blues', 'Greens', 'Oranges', 'Greys',
			'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
			'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
		# self.cmaps.items()[0][1]['Oranges'] = self.reverse_colourmap(self.cmaps.items()[0][1]['Oranges'])
		self.list_color = self.cmaps.items()[0][1]
		self.norm = matplotlib.colors.Normalize(vmin=MIN_VALUE_FREQUENCY, vmax=MAX_VALUE_FREQUENCY)
		self.color_dict = {}
		i = 0
		col = 0
		ap_cbs = dict()
		for name in self.AP:
			ap_cbs[name] = tk.Checkbutton(self.display2, text=name, onvalue=True, offvalue=False,font=("Arial",11))
			ap_cbs[name].config(background="#cdcdcd", borderwidth = 0, highlightthickness = 0)
			ap_cbs[name].var = tk.BooleanVar()
			ap_cbs[name]['variable'] = ap_cbs[name].var
			ap_cbs[name]['command'] = lambda w=ap_cbs[name]: self.upon_select(w)
			ap_cbs[name].grid(row=i, sticky=W)

			self.color_dict[name] = col
			cmap = plt.get_cmap(self.list_color[self.color_dict[name]])
			color = cmap(self.norm(MAX_VALUE_FREQUENCY))[:3]
			print(color,color[2]*255,color[1]*255,color[0]*255)
			ap_cbs[name].config(fg=matplotlib.colors.to_hex([color[0],color[1],color[2]]))
			i = i+1
			col = col+1
			if col >= len(self.list_color):
				col = 0

		self.display3 = tk.Frame(self.display2, width = 250, height = 50)
		self.display3.config(background="#cdcdcd")
		self.display3.grid(row=i, column=0, sticky="N", pady=40) #Display 3
		label_freq = Label(self.display3, text="Frequency:")
		label_freq.grid(row=0)
		label_freq.configure(background="#cdcdcd", pady=10,font=('Arial', 11, 'bold'))
		i = i+1
		butt_freq= tk.Checkbutton(self.display3, text="Use frequency [0,-100]", onvalue=True, offvalue=False,font=("Arial",11))
		butt_freq.config(background="#cdcdcd", borderwidth = 0, highlightthickness = 0)
		butt_freq.var = tk.BooleanVar()
		butt_freq['variable'] = butt_freq.var
		butt_freq['command'] = lambda w=butt_freq: self.select_frequency(w)
		butt_freq.grid(row=i, sticky=W)
		i = i+1

		self.display4 = tk.Frame(self.display2, width = 250, height = 50)
		self.display4.config(background="#cdcdcd")
		self.display4.grid(row=i, column=0,sticky="N") #Display 4

		# read image into matrix.
		self.map_image = cv2.imread(OFFICE_SVG_PATH)
		self.image_to_color = self.map_image
		self.useStandardFreq = False
		self.index_label_freq = 0
		self.label = dict()

	def select_frequency(self,widget):
		self.useStandardFreq = widget.var.get()
		if self.useStandardFreq == True:
			for wid in self.display4.winfo_children():
				wid.destroy()
		print("BUTTONN {}'s value is {}.".format(widget['text'], widget.var.get()))
		self.clear_label_image()
		self.image_to_color = self.map_image.copy()
		for i in self.AP_enabled:
			if self.useStandardFreq == False:
				self.create_label_frequency(i, self.AP[i])
			self.draw_circle(i)
			#print(i)
		self.resize_image()
		self.show_frame(self.resized_image)

	def upon_select(self, widget):
	    print("{}'s value is {}.".format(widget['text'], widget.var.get()))
	    address = self.AP[widget['text']]
	    if widget.var.get() == True:
			self.AP_enabled.append(widget['text'])
			self.draw_circle(widget['text'])
			self.create_label_frequency(widget['text'], address)
	    else:
			self.clear_label_image()
			self.AP_enabled.remove(widget['text'])
			self.image_to_color = self.map_image.copy()
			# self.display4.grid_forget()
			for wid in self.display4.winfo_children():
				wid.destroy()
			self.index_label_freq = 0
			for i in self.AP_enabled:
				self.create_label_frequency(i, self.AP[i])
				self.draw_circle(i)
				#print(i)
			self.resize_image()
			self.show_frame(self.resized_image)

	def create_label_frequency(self, name_ap, address):
		print("LABEL",name_ap,address)
		print("INDEX ",self.index_label_freq)
		label_str = name_ap +': ['+self.tuple_mapping[name_ap][1][address][1]+','+self.tuple_mapping[name_ap][1][address][0]+']'
		self.label[name_ap] = Label(self.display4, text=label_str)
		self.label[name_ap].grid(row=self.index_label_freq)
		self.index_label_freq= self.index_label_freq+1
		self.label[name_ap].configure(background="#cdcdcd", pady=2)
		self.window.grid_propagate(0)

	def draw_circle(self, name_ap):
	    # cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", self.cmaps.items()[0][1][self.color_dict[name_ap]])
	    cmap = plt.get_cmap(self.list_color[self.color_dict[name_ap]])
	    self.clear_label_image()
	    map_tmp = {}
	    if name_ap in self.mapping_AP:
			map_tmp = self.mapping_AP[name_ap]
	    else:
			self.tuple_mapping[name_ap] = self.map_manager.createMappingAP(self.AP[name_ap])
			map_tmp = self.tuple_mapping[name_ap][0].items()
			self.mapping_AP[name_ap] = map_tmp
	    if not self.useStandardFreq:
			MIN_VALUE_FREQUENCY = int(self.tuple_mapping[name_ap][1][self.AP[name_ap]][1])
			MAX_VALUE_FREQUENCY = int(self.tuple_mapping[name_ap][1][self.AP[name_ap]][0])
	    else:
			MIN_VALUE_FREQUENCY = -100
			MAX_VALUE_FREQUENCY = 0
	    norm = matplotlib.colors.Normalize(vmin=MIN_VALUE_FREQUENCY,
			vmax=MAX_VALUE_FREQUENCY)
	    for key, value in map_tmp:
			color = cmap(norm(value))[:3]
			#3450 tupla
			# x = self.w/2 - (int(((-1)*key[0])/self.resolution_value))
			# y = self.h/2 - (int((key[1])/self.resolution_value)) - 350
			y = self.w/2 - (int((key[0])/self.resolution_value)) 
			x = self.h/2 - (int((key[1])/self.resolution_value)) 
			# print("AFTER:", x, y)
			cv2.circle(self.image_to_color, (x,y), 2, (color[2]*255,color[1]*255,color[0]*255), -1)
	    self.resize_image()
			#check http://corecoding.com/utilities/rgb-or-hex-to-float.php
	    self.show_frame(self.resized_image)

	def get_info_image(self):
		# get image properties.
		self.h,self.w,self.bpp = np.shape(self.map_image)
		# print image properties.
		print "width: " + str(self.w)
		print "height: " + str(self.h)
		print "bpp: " + str(self.bpp)

	def resize_image(self):
		#center_x = self.w/2
		#center_y = self.h/2
		# self.image_to_color = self.map_image.copy()
		map_center = self.image_to_color[int(self.center_x-MAP_SIZE):int(self.center_x+MAP_SIZE), 
		int(self.center_y-MAP_SIZE):int(self.center_y+MAP_SIZE), :]
		r = 700.0 / map_center.shape[1]
		dim = (700, int(map_center.shape[0] * r))
		self.resized_image = cv2.resize(map_center, dim, interpolation = cv2.INTER_AREA)
		# self.resized_image = cv2.resize(map_center, (map_center.shape[0]*CONST_RESIZE,map_center.shape[1]*CONST_RESIZE),
		#  interpolation = cv2.INTER_AREA)
		self.w_res = self.resized_image.shape[0]*CONST_RESIZE
		self.h_res = self.resized_image.shape[1]*CONST_RESIZE
		# self.image_to_color = self.resized_image.copy()
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
		rows,cols,bpp = np.shape(self.map_image)
		M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
		self.map_image = cv2.warpAffine(self.map_image,M,(cols,rows))
		self.image_to_color = self.map_image.copy()
		self.resize_image()
		self.show_frame(self.resized_image)
		self.window.mainloop()  #Starts GUI

	def get_center(self):
		pattern = re.compile("origin")
		for _, line in enumerate(open(FILE_OFFICE_PATH)):
			for _ in re.finditer(pattern, line):
				self.center_x = float(line.split(":")[1].split(",")[1:][0])/self.resolution_value
				print(self.center_x)
				self.center_y = float(line.split(":")[1].split(",")[1])/self.resolution_value
				print(self.center_y)

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


	
	




