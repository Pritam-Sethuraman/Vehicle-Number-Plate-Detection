# Importing Necessary Modules and Libraries
import shutil
import os
import random
try:
 from PIL import Image
except ImportError:
 import Image
from google.colab.patches import cv2_imshow

# For Array Operations
import numpy as np

# For Image Processing
import imutils

# Open CV Library
import cv2

# Regex
import re

# Pytesseact Module
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# For Visualization in Python
import matplotlib.pyplot as plt


# Reading the image
rgbImage = cv2.imread('/content/KTM.jpg')
#rgbImage = cv2.resize(rgbImage, (400, 600))
plt.figure()
plt.imshow(cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB))
plt.title("Original Image")

# Coverting the RGB image to Grayscale
grayImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2GRAY)
plt.figure()
plt.imshow(grayImage, cmap='gray')
plt.title("Gray Image")

# Smoothening the Image
grayImage = cv2.bilateralFilter(grayImage, 13, 17, 17)
plt.figure()
plt.imshow(grayImage, cmap='gray')
plt.title("Smooth Gray Image")

# Defining the Thresholds
lowerThreshold = 30
upperThreshold = 3 * lowerThreshold

# Edge Detection
edgeDetectedImage = cv2.Canny(grayImage, lowerThreshold, upperThreshold)
plt.imshow(edgeDetectedImage, cmap='gray')
plt.title("Edge Detected Image")

# Finding Contours
contours, new = cv2.findContours(edgeDetectedImage.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
duplicateImage1 = rgbImage.copy()
cv2.drawContours(duplicateImage1, contours, -1, (0, 255, 0), 3)
plt.figure()
plt.imshow(duplicateImage1, cmap = 'gray')
plt.title("Canny Edge afer Contouring")

contours = sorted(contours, key = cv2.contourArea, reverse = True)[:30]
NumberPlateCount = None

duplicateImage2 = rgbImage.copy()
cv2.drawContours(duplicateImage2, contours, -1, (0, 255, 0), 3)
plt.figure()
plt.imshow(duplicateImage2, cmap = 'gray')
plt.title("Top 30 Contours")

count = 0
name = 1

for i in contours:
  perimeter = cv2.arcLength(i, True)
  approx = cv2.approxPolyDP(i, 0.02*perimeter, True)
  if(len(approx) == 4):
    NumberPlateCount = approx;
    x, y, w, h = cv2.boundingRect(i)
    cropedImage = rgbImage[y:y+h, x:x+w]
    cv2.imwrite(str(name) + '.png', cropedImage)
    name = name + 1
    break

cv2.drawContours(rgbImage, [NumberPlateCount], -1, (0, 255, 0), 3)
plt.figure()
plt.imshow(rgbImage, cmap = 'gray')
plt.title("Final Contour")

cropedImageLocation = '1.png'
plt.figure()
plt.imshow(cv2.imread(cropedImageLocation), cmap= 'gray')
plt.title("Cropped Image")

# Using Pytesseract to extract the text from the image
text = pytesseract.image_to_string(Image.open('1.png'))
tempPattern = r"\s+"
text1 = re.sub(tempPattern, "", text)

# Using Regex to extract the Licence Plate Number
finalText = re.findall("[a-zA-Z]{2}[0-9]{2}[a-zA-Z]{2}[0-9]{4}", text1)
print("Licence Plate Number: ", finalText)
