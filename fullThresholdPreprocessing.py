import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Show a file dialog to select an input image
file_path = filedialog.askopenfilename(title='Select Input Image', filetypes=(('JPEG files', '*.jpg'), ('PNG files', '*.png'), ('JPG files', '*.JPG'), ('All files', '*.*')))

# Load the selected image using OpenCV
if file_path:
    img = cv2.imread(file_path)

    # Convert the image to grayscale if it is not already in grayscale format
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # Resize the image to 256px (if not already 256px)
    if gray.shape[0] != 256 or gray.shape[1] != 256:
        gray = cv2.resize(gray, (256, 256))

    # Apply Gaussian smoothing filter
    kernel_size=5
    sigma=0
    smoothed = cv2.GaussianBlur(gray, (kernel_size, kernel_size), sigma)

    # Apply adaptive thresholding
    adaptive_thresh = cv2.adaptiveThreshold(smoothed, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Apply morphological opening to remove small artifacts
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opened = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_OPEN, kernel)

    # Perform contour detection on the opened image
    contours, hierarchy = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the original image
    contours_img = img.copy()
    cv2.drawContours(contours_img, contours, -1, (0, 255, 0), 3)

    # Calculate texture features using Haralick texture analysis
    gray = cv2.cvtColor(contours_img, cv2.COLOR_BGR2GRAY)
    texture_features = cv2.calcHist([gray], [0], None, [256], [0, 256])
    texture_features = cv2.normalize(texture_features, texture_features).flatten()

    # Calculate intensity-based features
    intensity_features = []
    intensity_features.append(np.mean(gray))
    intensity_features.append(np.var(gray))
    intensity_features.append(np.std(gray))
    intensity_features.append(np.min(gray))
    intensity_features.append(np.max(gray))

    # Display the original image, the image with contours, and the texture and intensity features
    cv2.imshow('Original Image', img)
    cv2.imshow('Image with Contours', contours_img)
    print('Texture Features:', texture_features)
    print('Intensity Features:', intensity_features)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
