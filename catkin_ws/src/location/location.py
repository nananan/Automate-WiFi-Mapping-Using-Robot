#!/usr/bin/env python

import cv2
import Tkinter as tk
from Tkinter import *
from PIL import Image
from PIL import ImageTk

import numpy as np
# from mercator import *


OFFICE_SVG_PATH = '../navigation/mybot_navigation/maps/ufficio.pgm'
# PIXEL = 37.7952755906

CONST_RESIZE = 5
MAP_SIZE = 50

class GUI_Manager:
	def __init__(self):
		#Set up GUI
		self.window = tk.Tk()  #Makes main window
		self.window.wm_title("Mapping Tino")
		self.window.config(background="#FFFFFF")

		#Graphics window
		self.imageFrame = tk.Frame(self.window, width=600, height=500)
		self.imageFrame.grid(row=0, column=0, padx=10, pady=2)

		self.display1 = tk.Label(self.imageFrame)
		self.display1.grid(row=0, column=0) #, padx=10, pady=2)  #Display 1
		self.display2 = tk.Frame(self.window, width = 300, height = 100, relief = 'raised')
		self.display2.grid(row=0, column=1) #Display 2

		i = 0
		names = {"AAA", "BBB", "CCC"}
		username_cbs = dict()
		for name in names:
			username_cbs[name] = tk.Checkbutton(self.display2, text=name, onvalue=True, offvalue=False)
			username_cbs[name].var = tk.BooleanVar()
			username_cbs[name]['variable'] = username_cbs[name].var
			username_cbs[name]['command'] = lambda w=username_cbs[name]: self.upon_select(w)
			username_cbs[name].grid(row=i, sticky=W)
			i = i+1
			# username_cbs[name].pack()
		# read image into matrix.
		self.map_image = cv2.imread(OFFICE_SVG_PATH)

	def upon_select(self, widget):
	    print("{}'s value is {}.".format(widget['text'], widget.var.get()))

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
		map_center = self.map_image[center_y-MAP_SIZE:center_y+MAP_SIZE, center_x-MAP_SIZE:center_x+MAP_SIZE, :]

		self.resized_image = cv2.resize(map_center, (map_center.shape[0]*CONST_RESIZE,map_center.shape[1]*CONST_RESIZE),
		 interpolation = cv2.INTER_AREA)

	def find_rgb(self, imagename, r_query, g_query, b_query):
		img = Image.open(imagename)
		rgb = img.convert('RGB')
		for x in range(img.size[0]):
			for y in range(img.size[1]):
				r, g, b, = rgb.getpixel((x, y))
				if r == r_query and g == g_query and b == b_query:
					return (x,y)


	def show_frame(self):
		cv2image = cv2.cvtColor(self.resized_image, cv2.COLOR_BGR2RGBA)
		img = Image.fromarray(cv2image)
		imgtk = ImageTk.PhotoImage(image=img)
		self.display1.imgtk = imgtk #Shows frame for display 1
		self.display1.configure(image=imgtk)
		# window.after(10, show_frame) 

	def update(self):
		self.show_frame()
		self.window.mainloop()  #Starts GUI

if __name__ == "__main__":
	gui_manager = GUI_Manager()
	gui_manager.get_info_image()
	gui_manager.resize_image()

	gui_manager.update()


	
	




