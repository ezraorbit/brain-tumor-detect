import numpy as np 
from tqdm import tqdm
import cv2
import os
import imutils


IMG_SIZE = 256

def crop_img(img):
	# Check if the image was successfully loaded
	if img is None:
		raise FileNotFoundError(f"Error: Unable to load the image")

	img = cv2.imread(img)

	# Your existing image cropping code
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (3, 3), 0)

	# threshold the image, then perform a series of erosions +
	# dilations to remove any small regions of noise
	thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.erode(thresh, None, iterations=2)
	thresh = cv2.dilate(thresh, None, iterations=2)

	# find contours in thresholded image, then grab the largest one
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key=cv2.contourArea)

	# find the extreme points
	extLeft = tuple(c[c[:, :, 0].argmin()][0])
	extRight = tuple(c[c[:, :, 0].argmax()][0])
	extTop = tuple(c[c[:, :, 1].argmin()][0])
	extBot = tuple(c[c[:, :, 1].argmax()][0])
	ADD_PIXELS = 0
	new_img = img[extTop[1]-ADD_PIXELS:extBot[1]+ADD_PIXELS, extLeft[0]-ADD_PIXELS:extRight[0]+ADD_PIXELS].copy()

	#resize image
	new_img = cv2.resize(new_img,(IMG_SIZE,IMG_SIZE))
	
	#Save the cropped image
	output_folder = "./output"
	os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
	output_path = os.path.join(output_folder, "output.jpg")
	cv2.imwrite(output_path, new_img)

	return new_img
