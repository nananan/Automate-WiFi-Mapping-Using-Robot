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
import re,os,argparse
import imp
file = os.path.dirname(os.path.abspath(__file__))
mapping_man = imp.load_source('Mapping',file+'/waypoint/mapping.py')


MAP_IMAGE_PATH = file+'/../navigation/mybot_navigation/map_cubo/corridoio_all_good.pgm'
MAP_YAML_PATH = file+'/../navigation/mybot_navigation/map_cubo/corridoio_all_good.yaml'
IMAGE_ICON = file+'/img/wifi_icon.png'
# PIXEL = 37.7952755906
BACKGROUND_COLOR = "#a2b6ca" #"#6799c7"
BACKGROUND_COLOR_MENU = "#d2dbe5"
CONST_RESIZE = 1
CONST_RESIZE_CIRCLE = 1
MAP_SIZE = 400
MIN_VALUE_FREQUENCY = -80
MAX_VALUE_FREQUENCY = -50

class GUI_Manager:
	def __init__(self):
		if not self.get_params():
			os._exit(0)
		self.map_image_path = self.args.map_image if self.args.map_image else MAP_IMAGE_PATH
		self.map_yaml_path = self.args.map_yaml if self.args.map_yaml else MAP_YAML_PATH
		#Get resolution value of the map image
		self.resolution_value = self.get_resolution()
		self.get_center()
		#Create APs list
		self.map_manager = mapping_man.Mapping()
		self.AP = self.map_manager.getAPs()
		self.AP_enabled = []
		self.mapping_AP = {}

		#Set up GUI
		self.window = tk.Tk()  #Makes main window
		self.window.wm_title("Mapping Tino")
		self.window.resizable()
		self.window.maxsize()
		imgicon = PhotoImage(file=IMAGE_ICON)
		self.window.tk.call('wm','iconphoto', self.window._w, imgicon)
		self.window.config(background=BACKGROUND_COLOR)

		#Graphics window
		self.imageFrame = tk.Frame(self.window, width=900, height=500)
		self.imageFrame.pack(side=LEFT, padx=10, pady=10)#grid(row=0, column=0, padx=10, pady=10)
		self.display1 = tk.Label(self.imageFrame, borderwidth = 0, highlightthickness = 0)#, width=800, height=500)
		self.display1.pack(side=LEFT)#grid(row=0, column=0) #, padx=10, pady=2)  #Display 1

		#SHADOW
		# self.display2_sh = tk.Frame(self.window)
		# self.display2_sh.config(background="#82868a", borderwidth = 0, highlightthickness = 0, width=301, height=512)
		# self.display2_sh.grid(row=0, column=1, sticky="N", padx=50, pady=20) #Display 2
		# self.display2_sh.grid_propagate(False)

		self.display2 = tk.Canvas(self.window)
		self.display2.config(background=BACKGROUND_COLOR_MENU, borderwidth=2, relief="raised", width=280, height=510)
		#flat, groove, raised, ridge, solid, or sunken
		self.display2.pack(side=RIGHT,fill=NONE, expand=1, padx=20, pady=10)#grid(row=0, column=1, sticky="N", padx=50, pady=20) #Display 2
		self.display2.grid_propagate(0)
		# self.display2.create_arc(710, 300, 840, 300,style='arc', width=300)

		self.tuple_mapping = dict()
		self.cmaps = OrderedDict()

		self.cmaps['Sequential'] = [
			'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
			'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
			'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
			#Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Vega10, Vega10_r, Vega20, Vega20_r, Vega20b, Vega20b_r, Vega20c, Vega20c_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spectral, spectral_r, spring, spring_r, summer, summer_r, terrain, terrain_r, viridis, viridis_r, winter, winter_r
		# self.cmaps.items()[0][1]['Oranges'] = self.reverse_colourmap(self.cmaps.items()[0][1]['Oranges'])
		self.list_color = self.cmaps.items()[0][1]
		self.norm = matplotlib.colors.Normalize(vmin=MIN_VALUE_FREQUENCY, vmax=MAX_VALUE_FREQUENCY)
		self.color_dict = {}

		label_list_wifi = Label(self.display2, text="List Wireless Source:")
		label_list_wifi.grid(row=0, sticky="W", padx=3, pady=3)
		label_list_wifi.configure(background=BACKGROUND_COLOR_MENU, font=('Arial', 11, 'bold'))
		frame_ap=Frame(self.display2,width=100,height=500)
		# frame_ap.configure(borderwidth=2, relief="raised")
		frame_ap.grid(row=1,column=0, padx=3)

		scrollbar_ap = Scrollbar(frame_ap,bg=BACKGROUND_COLOR)
		scrollbar_ap.pack(side=RIGHT, fill=Y)

		self.display_ap=Canvas(frame_ap,bg=BACKGROUND_COLOR_MENU)
		self.display_ap.configure(width=250,height=180, borderwidth = 0, highlightthickness = 0)
		self.display_ap.configure(scrollregion=(0,0,250,len(self.AP)*20), yscrollcommand=scrollbar_ap.set)
		self.display_ap.pack(fill='both', expand=True, side='left')

		scrollbar_ap.config(command=self.display_ap.yview)
		i = 0
		col = 0
		self.ap_cbs = dict()
		for address in self.AP:
			name = self.AP[address]
			widget = tk.Checkbutton(self.display_ap, text=name, onvalue=True, offvalue=False,font=("Arial",11))
			widget.config(background=BACKGROUND_COLOR_MENU, borderwidth = 0, highlightthickness = 0)

			widget.var = tk.BooleanVar()
			widget['variable'] = widget.var
			widget['command'] = lambda w=widget: self.upon_select(w)
			widget.grid(row=i, sticky=W)
			self.ap_cbs[widget] = address
			self.display_ap.create_window(0, i*20, anchor='nw', window=widget, height=20)

			self.color_dict[address] = col
			cmap = plt.get_cmap(self.list_color[self.color_dict[address]])
			color = cmap(self.norm(MAX_VALUE_FREQUENCY))[:3]
			print(color,color[2]*255,color[1]*255,color[0]*255)
			widget.config(fg=matplotlib.colors.to_hex([color[0],color[1],color[2]]))
			i = i+1
			col = col+1
			if col >= len(self.list_color):
				col = 0

		i = i+1
		self.display_button = tk.Frame(self.display2)
		self.display_button.configure(background=BACKGROUND_COLOR_MENU, width=250, height=50)
		self.display_button.grid(row=i, column=0, sticky="E", pady=10) #Display 3
		self.display_button.grid_propagate(0)
		desel_all = Button(self.display_button, command=self.deselect_all, text="Deselect All",font=('Arial', 10, 'bold'))
		desel_all.pack(side=RIGHT)#grid(row=0, column = 1, sticky=E)
		desel_all.config(relief=FLAT, background=BACKGROUND_COLOR_MENU, borderwidth = 0, highlightthickness = 0)
		sel_all = Button(self.display_button, command=self.select_all, text="Select All",font=('Arial', 10, 'bold'))
		sel_all.pack(side=RIGHT)#grid(row=0, column = 0, sticky=E)
		sel_all.config(relief=FLAT, background=BACKGROUND_COLOR_MENU, borderwidth = 0, highlightthickness = 0)
		i = i+1

		self.display3 = tk.Frame(self.display2, width=250, height=50)
		self.display3.config(background=BACKGROUND_COLOR_MENU)
		self.display3.grid(row=i, column=0, sticky="NW", pady=3, padx=3) #Display 3
		self.display3.grid_propagate(0)
		label_freq = Label(self.display3, text="Power:")
		label_freq.grid(row=0, sticky="W", pady=3)
		label_freq.configure(background=BACKGROUND_COLOR_MENU,font=('Arial', 11, 'bold'))
		i = i+1
		butt_freq = tk.Checkbutton(self.display3, text="Use Power range [-100,0]", onvalue=True, offvalue=False,font=("Arial",11))
		butt_freq.config(background=BACKGROUND_COLOR_MENU, borderwidth = 0, highlightthickness = 0)
		butt_freq.var = tk.BooleanVar()
		butt_freq['variable'] = butt_freq.var
		butt_freq['command'] = lambda w=butt_freq: self.select_power_streght(w)
		butt_freq.grid(row=i, sticky="W", padx=10)
		i = i+1
		label_freq_range = Label(self.display2, text="Power Ranges:")
		label_freq_range.grid(row=i, sticky="NW", padx=3, pady=3) #grid(row=0, padx=3, pady=3)#
		label_freq_range.configure(background=BACKGROUND_COLOR_MENU,font=('Arial', 10, 'bold'))
		i=i+1
		frame=Frame(self.display2,width=100,height=500)
		frame.grid(row=i,column=0)

		scrollbar = Scrollbar(frame,bg=BACKGROUND_COLOR)
		scrollbar.pack(side=RIGHT, fill=Y)

		self.display4=Canvas(frame,bg=BACKGROUND_COLOR_MENU, borderwidth = 0, highlightthickness = 0)
		self.display4.configure(width=250,height=130)
		self.display4.configure(scrollregion=(0,0,250,len(self.AP)*20), yscrollcommand=scrollbar.set)
		self.display4.pack(fill='both', expand=True, side='left')

		scrollbar.config(command=self.display4.yview)

		h = "cdcdcd".lstrip('#')
		col_back = tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

		h = BACKGROUND_COLOR.lstrip('#')
		col_back_new = tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))
		print(col_back_new[0],col_back_new[1],col_back_new[2])
		# read image into matrix.
		self.map_image = cv2.imread(self.map_image_path)
		self.map_image[np.where((self.map_image == [col_back[2],col_back[1],col_back[0]])
			.all(axis = 2))] = col_back_new[2],col_back_new[1],col_back_new[0]

		self.image_to_color = self.map_image
		self.useStandardFreq = False
		self.index_label_freq = 0
		self.label = dict()
		self.destroy_child = False

	def get_params(self):
		parser = argparse.ArgumentParser(description='location.py')
		parser.add_argument('-i', '--map_image', dest='map_image', type=str, required=False, help='Path of image of the map')
		parser.add_argument('-y', '--map_yaml', dest='map_yaml', type=str, required=False, help='Path of file yaml of the map')
		self.args = parser.parse_args()
		user = os.getenv("SUDO_USER")

		if user is None:
			print("This program needs 'sudo'")
			return False
		else:
			print('Press CTRL+c to stop sniffing...')
			return True


	def select_power_streght(self, widget):
		self.useStandardFreq = widget.var.get()
		if self.useStandardFreq == True:
			for wid in self.display4.winfo_children():
				wid.destroy()
				self.destroy_child = True
		# else:
		# 	label_freq_range = Label(self.display4, text="Power Ranges:")
		# 	label_freq_range.pack(side=TOP, padx=3, pady=3) #grid(row=0, padx=3, pady=3)#
		# 	label_freq_range.configure(background=BACKGROUND_COLOR_MENU,font=('Arial', 10, 'bold'))
		# print("BUTTONN {}'s value is {}.".format(widget['text'], widget.var.get()))
		self.clear_label_image()
		self.image_to_color = self.map_image.copy()
		for i in self.AP_enabled:
			if self.useStandardFreq == False:
				self.create_label_power(self.AP[i], i)
			self.draw_circle(i)
			#print(i)
		self.resize_image()
		self.show_frame(self.resized_image)

	def upon_select(self, widget):
	    print("{}'s value is {}.".format(self.ap_cbs[widget], widget.var.get()))
	    address = self.ap_cbs[widget]
	    # for ap in self.AP:
		# 	if self.AP[ap] == widget['text']:
		# 	    address = ap
		# 	    pass
	    if widget.var.get() == True:
			self.AP_enabled.append(address)
			self.draw_circle(address)
			self.destroy_child = True
			self.create_label_power(widget['text'], address)
	    else:
			self.clear_label_image()
			self.AP_enabled.remove(address)
			self.image_to_color = self.map_image.copy()
			# self.display4.grid_forget()
			for wid in self.display4.winfo_children():
				wid.destroy()
				self.destroy_child = True
			self.index_label_freq = 0
			for i in self.AP_enabled:
				self.create_label_power(self.AP[i], i)
				self.draw_circle(i)
				#print(i)
			self.resize_image()
			self.show_frame(self.resized_image)

	def create_label_power(self, name_ap, address):
		# print("LABEL",name_ap,address)
		# print("INDEX ",self.index_label_freq)
		if self.useStandardFreq:
			return
		else:
			# if self.destroy_child:
			# 	label_freq_range = Label(self.display4, text="Power Ranges:")
			# 	label_freq_range.pack(side=TOP, padx=3, pady=3) #grid(row=0, padx=3, pady=3)#
			# 	label_freq_range.configure(background=BACKGROUND_COLOR_MENU,font=('Arial', 10, 'bold'))
			# 	self.destroy_child = False
			label_str = name_ap +': ['+self.tuple_mapping[address][1][address][1]+','+self.tuple_mapping[address][1][address][0]+']'
			self.label[address] = Label(self.display4, text=label_str)
			# self.label[address].pack(side=TOP, padx=5) #grid(row=self.index_label_freq, padx=5) #
			cmap = plt.get_cmap(self.list_color[self.color_dict[address]])
			color = cmap(self.norm(MAX_VALUE_FREQUENCY))[:3]
			self.label[address].config(fg=matplotlib.colors.to_hex([color[0],color[1],color[2]]))
			self.label[address].configure(background=BACKGROUND_COLOR_MENU, pady=2, padx=10)

			self.display4.create_window(0, self.index_label_freq*20, anchor='nw', window=self.label[address], height=20)
			self.index_label_freq = self.index_label_freq+1
			self.window.grid_propagate(0)

	def select_all(self):
		for ap in self.AP:
			self.draw_circle(ap)
			self.ap_cbs.keys()[self.ap_cbs.values().index(ap)].var.set(True)
			self.AP_enabled.append(ap)
			self.destroy_child = True
			self.create_label_power(self.AP[ap], ap)

	def deselect_all(self):
		self.clear_label_image()
		self.image_to_color = self.map_image.copy()
		for wid in self.display4.winfo_children():
			wid.destroy()
		self.index_label_freq = 0
		for ap in self.AP:
			if ap in self.AP_enabled:
				self.AP_enabled.remove(ap)
			self.ap_cbs.keys()[self.ap_cbs.values().index(ap)].var.set(False)
		self.resize_image()
		self.show_frame(self.resized_image)

	def draw_circle(self, name_ap):
	    # cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", self.cmaps.items()[0][1][self.color_dict[name_ap]])
	    cmap = plt.get_cmap(self.list_color[self.color_dict[name_ap]])
	    self.clear_label_image()
	    map_tmp = {}
	    if name_ap in self.mapping_AP:
			map_tmp = self.mapping_AP[name_ap]
	    else:
			self.tuple_mapping[name_ap] = self.map_manager.createMappingAP(name_ap)
			map_tmp = self.tuple_mapping[name_ap][0].items()
			self.mapping_AP[name_ap] = map_tmp
	    if not self.useStandardFreq:
			MIN_VALUE_FREQUENCY = int(self.tuple_mapping[name_ap][1][name_ap][1])
			MAX_VALUE_FREQUENCY = int(self.tuple_mapping[name_ap][1][name_ap][0])
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
		map_center = self.image_to_color[int(self.center_x-MAP_SIZE/2.5):int(self.center_x+MAP_SIZE/2.5),
		int(self.center_y-MAP_SIZE/4):int(self.center_y+MAP_SIZE), :]
		r = 850.0 / map_center.shape[1]
		dim = (850, int(map_center.shape[0] * r))
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
		for _, line in enumerate(open(self.map_yaml_path)):
			for _ in re.finditer(pattern, line):
				self.center_x = float(line.split(":")[1].split(",")[1:][0])/self.resolution_value
				print(self.center_x)
				self.center_y = float(line.split(":")[1].split(",")[1])/self.resolution_value
				print(self.center_y)

	def get_resolution(self):
		pattern = re.compile("resolution")
		for _, line in enumerate(open(self.map_yaml_path)):
			for _ in re.finditer(pattern, line):
				return float(line.split(":")[1][:-1])

if __name__ == "__main__":
	gui_manager = GUI_Manager()
	gui_manager.get_info_image()
	gui_manager.resize_image()

	gui_manager.update()
	# plastik_image_dir='img/'
	# root = Tkinter.Tk()
	# plastik_theme.install(plastik_image_dir)
