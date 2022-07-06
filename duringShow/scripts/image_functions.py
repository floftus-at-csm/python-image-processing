from PIL import Image, ImageOps
import os
from os import path
import random
from random import randint

import skimage
from skimage import data, transform, exposure
from skimage.util import compare_images
import numpy as np

global prepared
prepared=1

# def resize_the_file(msg, dir_path):
# 	img = Image.open(os.path.join(dir_path, 'stitched', str(msg)+'.jpg'))
# 	new_img = img.resize((648, int(480/3)), Image.ANTIALIAS)
# 	new_img.save(os.path.join(dir_path, 'resized', str(msg)+'.jpg'))
def resize_the_file(msg, dir_path):
	height = 480
	width = 648
	img = Image.open(os.path.join(dir_path, 'stitched', str(msg)+'.jpg'))
	new_img = img.resize((width, height), Image.ANTIALIAS)
	new_img.save(os.path.join(dir_path, 'resized', str(msg)+'.jpg'))

def combine_three_images(msg, dir_path, prepared):
	image1 = Image.open(os.path.join(dir_path, 'resized', str(msg)+'.jpg'))
	# random1 = randint(msg-2, msg-1)
	# random2 = randint(1, msg-1)
	# image2 = Image.open(os.path.join(dir_path, 'resized', str(random1)+'.jpg'))
	image2 = Image.open(os.path.join(dir_path, 'resized', str(msg-1)+'.jpg'))
	# image3 = Image.open(os.path.join(dir_path, 'resized', str(random2)+'.jpg'))
	image3 = Image.open(os.path.join(dir_path, 'resized', str(msg-2)+'.jpg'))
	images = [image1, image2, image3]
	height = 480
	width = 648
	new_im = Image.new('RGB', (width, height))
	y_offset = 0
	new_im.paste(image1, (0, 0)) 
	y_offset+height/3
	new_im.paste(image2, (0, 160))
	y_offset+height/3
	new_im.paste(image3, (0, 320))
	# y_offset = 0
	# for im in images:
	# 	new_im.paste(im, (0, y_offset))
	# 	y_offset+height/3
	new_im.save(os.path.join(dir_path, 'prepared', str(prepared)+'.jpg'))
	# testing both ways rsync
	# new_im.save(os.path.join(dir_path, 'stitched', 'prepared', str(prepared)+'.jpg'))
	prepared=prepared+1


# def resize():
# 	#things go here

# def layer(prepared, dir_path, prepared_diff):
# 	print('this is the layer function')
# 	print('this is the layer function')
# 	print('this is the layer function')
# 	print('prepared: ')
# 	print(prepared)
# 	print('prepared diff: ')
# 	print(prepared_diff)
# 	#do things here
# 	# this should use skimage to create a difference from the previous one 
# 	# and then save it to 'prepared_difference'
# 	try:
# 		prepared_diff_directory = os.path.join(dir_path, 'prepared_diff')
# 		if not os.path.exists(prepared_diff_directory):
# 			os.makedirs(prepared_diff_directory)
# 		image = os.path.join(dir_path, 'prepared', str(prepared)+'.jpg')
# 		img1 = io.imread(image, as_gray=True)
# 		img1_equalized = exposure.equalize_hist(img1)
# 		if len(os.listdir(prepared_diff_directory)) == 0:
# 			prepared_earlier = prepared-1
# 			image2 = os.path.join(dir_path, 'prepared', str(prepared_earlier)+'.jpg')
# 			img2 = io.imread(image2, as_gray=True)
# 		else:
# 			image2 = os.path.join(dir_path, 'prepared_diff', str(prepared_diff)+'.jpg')
# 			img2 = io.imread(image2, as_gray=True)
# 		differenced_image = compare_images(img1, img2, method='diff')
# 		prepared_diff=prepared_diff+1
# 		output_path=os.path.join(prepared_diff_directory, str(prepared_diff)+'.jpg')
# 		io.imsave(output_path, differenced_image)

# 	except:
# 		print("no prepared_diff available")

def layer(msg, dir_path,layer):
	try:
		print("msg is:")
		print(msg)
		image = os.path.join(dir_path, 'stitched', str(msg)+'.jpg')
		img1 = io.imread(image, as_gray=True)
		img1_equalized = exposure.equalize_hist(img1)
		image2 = os.path.join(dir_path, 'stitched', str(msg-1)+'.jpg')
		img2 = io.imread(image2, as_gray=True)
		differenced_image = compare_images(img1, img2, method='diff')
		output_path=os.path.join(dir_path, 'layered', (layer)+'.jpg')
		io.imsave(output_path, differenced_image)

	except:
		print("no prepared_diff available")


def crop_from_resized(msg, dir_path, prepared):
	# take resized image - crop
	height = 480
	width = 648
	image = Image.open(os.path.join(dir_path, 'resized', str(msg)+'.jpg'))
	top_left = randint(0, (2*width))
	print(top_left)
	border = (top_left, 0, top_left+width, 0) # left, top, right, bottom
	cropped_image = ImageOps.crop(image, border)
	cropped_image.save(os.path.join(dir_path, 'prepared', str(prepared)+'.jpg'))
# def crop_from_full():
# 	# take full image - crop randomly
# 	# save to prepared