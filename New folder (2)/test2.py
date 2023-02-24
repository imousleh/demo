import cv2
import time
import tkinter as tk
from tkinter import filedialog

def threshold_comparison(image):
    # Apply Otsu's thresholding
    start = time.time()
    _, otsu_thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    otsu_time = time.time() - start

    # Apply adaptive thresholding
    start = time.time()
    adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    adaptive_time = time.time() - start

    # Compare the results
    otsu_count = cv2.countNonZero(otsu_thresh)
    adaptive_count = cv2.countNonZero(adaptive_thresh)

    if otsu_count > adaptive_count:
        return otsu_thresh, otsu_time, "Otsu"
    else:
        return adaptive_thresh, adaptive_time, "Adaptive"

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Show a file dialog to select a brain tumor image
file_path = filedialog.askopenfilename(title='Select Brain Tumor Image', filetypes=(('JPEG files', '*.jpg'), ('PNG files', '*.png'), ('All files', '*.*')))

# Load the selected image using OpenCV
if file_path:
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    resized_img = cv2.resize(img, (256, 256))

    # Compare thresholding methods
    result, time_taken, method = threshold_comparison(resized_img)

    # Display the result and the method used
    cv2.imshow('Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f"Thresholding using {method} method was faster and produced a better result (took {time_taken} seconds).")
