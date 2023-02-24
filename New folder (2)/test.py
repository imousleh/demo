import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Function to open file dialog and select image
def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=(("Image Files", "*.jpg;*.jpeg;*.png"), ("All Files", "*.*")))
    return file_path

# Load image
img_path = select_image()
img = cv2.imread(img_path)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian smoothing filter
kernel_size=5
sigma=0
smoothed = cv2.GaussianBlur(gray, (kernel_size, kernel_size), sigma)

# Apply adaptive thresholding
adaptive_thresh = cv2.adaptiveThreshold(smoothed, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

# Apply morphological opening to remove small artifacts
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
opened = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_OPEN, kernel)

# Find contours
contours, hierarchy = cv2.findContours(opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on original image
contour_img = img.copy()
cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)

# cv2.drawContours(contour_img, contours, -1, (0, 0, 255), 3)

# Display original image and contour image side by side in a GUI
win_name = "Threshold and Contours"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.imshow(win_name, np.hstack([img, contour_img]))
cv2.waitKey(0)
cv2.destroyAllWindows()
