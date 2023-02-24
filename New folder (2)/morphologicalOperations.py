import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def threshold_segmentation(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply simple thresholding
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Apply adaptive thresholding
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Combine the two thresholded images
    combined_thresh = cv2.bitwise_or(thresh, adaptive_thresh)

    # Perform morphological operations
    kernel = np.ones((3, 3), np.uint8)
    eroded = cv2.erode(combined_thresh, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=1)

    return dilated


# Create a GUI to select and display the image
def select_image():
    # Open a file dialog to select an image
    file_path = filedialog.askopenfilename()

    # Load the image using OpenCV
    image = cv2.imread(file_path)

    # Apply the thresholding and morphological segmentation
    segmented_image = threshold_segmentation(image)

    # Convert the OpenCV image to a PIL image and then to a PhotoImage for display in the GUI
    segmented_image = Image.fromarray(segmented_image)
    segmented_image = ImageTk.PhotoImage(segmented_image)

    # Create a new window to display the image
    window = tk.Toplevel()
    window.title("Segmented Image")

    # Add the segmented image to the window
    label = tk.Label(window, image=segmented_image)
    label.pack()

    # Run the GUI
    window.mainloop()

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
    
    # Show the filtered image
    cv2.imshow('Smoothed MRI Image', smoothed)

    # Save the filtered image
    save_path = filedialog.asksaveasfilename(title='Save Smoothed MRI Image', defaultextension='.png', filetypes=(('JPEG files', '*.jpg'), ('PNG files', '*.png'), ('JPG files', '*.JPG'), ('All files', '*.*')))
    if save_path:
        cv2.imwrite(save_path, smoothed)

    # Set the resolution to 300dpi
    with Image.open(save_path) as image:
        dpi = (300, 300)
        image.info['dpi'] = dpi
        image.save(save_path)
