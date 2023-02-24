import cv2
import mahotas
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

    # Apply contour detection
    contours, hierarchy = cv2.findContours(adaptive_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    # Compute Haralick texture features
    textures = mahotas.features.haralick(gray)
    ht_mean = textures.mean(axis=0)

    # Show the contour image
    cv2.imshow('Contour Detected MRI Image', img)

    # Save the contour image
    save_path = filedialog.asksaveasfilename(title='Save Contour Detected MRI Image', defaultextension='.png', filetypes=(('JPEG files', '*.jpg'), ('PNG files', '*.png'), ('JPG files', '*.JPG'), ('All files', '*.*')))
    if save_path:
        cv2.imwrite(save_path, img)

    # Show the computed Haralick texture features
    print('Haralick Texture Features (mean):', ht_mean)

    # Set the resolution to 300dpi
    with Image.open(save_path) as image:
        dpi = (300, 300)
        image.info['dpi'] = dpi
        image.save(save_path)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
