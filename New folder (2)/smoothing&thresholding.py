import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Show a file dialog to select a brain tumor image
file_path = filedialog.askopenfilename(title='Select Brain Tumor Image', filetypes=(('JPEG files', '*.jpg'), ('PNG files', '*.png'), ('JPG files', '*.JPG'), ('All files', '*.*')))

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

    # Show the filtered image
    cv2.imshow('Adaptive Thresholded MRI Image', adaptive_thresh)

    # Save the filtered image
    save_path = filedialog.asksaveasfilename(title='Save Adaptive Thresholded MRI Image', defaultextension='.png', filetypes=(('JPEG files', '*.jpg'), ('PNG files', '*.png'), ('JPG files', '*.JPG'), ('All files', '*.*')))
    if save_path:
        cv2.imwrite(save_path, adaptive_thresh)

    # Set the resolution to 300dpi
    with Image.open(save_path) as image:
        dpi = (300, 300)
        image.info['dpi'] = dpi
        image.save(save_path)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
