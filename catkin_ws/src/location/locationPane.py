#!/usr/bin/env python
# import the necessary packages
# from Tkinter import *
# from PIL import Image
# from PIL import ImageTk
# import tkFileDialog
# import cv2

# def select_image():
# 	# grab a reference to the image panels
# 	global panelA, panelB

# 	# open a file chooser dialog and allow the user to select an input
# 	# image
# 	path = tkFileDialog.askopenfilename()

# 	# ensure a file path was selected
# 	if len(path) > 0:
# 		# load the image from disk, convert it to grayscale, and detect
# 		# edges in it
# 		image = cv2.imread(path)
# 		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 		edged = cv2.Canny(gray, 50, 100)

# 		# OpenCV represents images in BGR order; however PIL represents
# 		# images in RGB order, so we need to swap the channels
# 		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 		# convert the images to PIL format...
# 		image = Image.fromarray(image)
# 		edged = Image.fromarray(edged)

# 		# ...and then to ImageTk format
# 		image = ImageTk.PhotoImage(image)
# 		edged = ImageTk.PhotoImage(edged)

# 		# if the panels are None, initialize them
# 		if panelA is None or panelB is None:
# 			# the first panel will store our original image
# 			panelA = Label(image=image)
# 			panelA.image = image
# 			panelA.pack(side="left", padx=10, pady=10)

# 			# while the second panel will store the edge map
# 			panelB = Label(image=edged)
# 			panelB.image = edged
# 			panelB.pack(side="right", padx=10, pady=10)

# 		# otherwise, update the image panels
# 		else:
# 			# update the pannels
# 			panelA.configure(image=image)
# 			panelB.configure(image=edged)
# 			panelA.image = image
# 			panelB.image = edged

# # initialize the window toolkit along with the two image panels
# root = Tk()
# panelA = None
# panelB = None

# # create a button, then when pressed, will trigger a file chooser
# # dialog and allow the user to select an input image; then add the
# # button the GUI
# btn = Button(root, text="Select an image", command=select_image)
# btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

# # kick off the GUI
# root.mainloop()



#!/usr/bin/env python

import cv2
import Tkinter as tk

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from colorspacious import cspace_converter
from collections import OrderedDict

cmaps = OrderedDict()

cmaps['Sequential'] = [
	'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
	'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
	'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
nrows = max(len(cmap_list) for cmap_category, cmap_list in cmaps.items())
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

def plot_color_gradients(cmap_category, cmap_list, nrows):
    fig, axes = plt.subplots(nrows=nrows)
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99)
    axes[0].set_title(cmap_category + ' colormaps', fontsize=14)

    for ax, name in zip(axes, cmap_list):
        print("AAAAAA ",name, cmap_list[0])
        ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax.set_axis_off()


print(cmaps.items()[0][1][0])
for cmap_category, cmap_list in cmaps.items():
    print(cmap_list)
    plot_color_gradients(cmap_category, cmap_list, nrows)

plt.show()

