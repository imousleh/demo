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

    return combined_thresh


# Create a GUI to select and display the image
def select_image():
    # Open a file dialog to select an image
    file_path = filedialog.askopenfilename()

    # Load the image using OpenCV
    image = cv2.imread(file_path)

    # Apply the thresholding segmentation
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

# Create a button to launch the GUI
root = tk.Tk()
button = tk.Button(root, text="Select Image", command=select_image)
button.pack()

# Run the main loop
root.mainloop()
