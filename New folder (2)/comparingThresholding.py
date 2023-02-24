import cv2
import time
import tkinter as tk
from tkinter import filedialog

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Show a file dialog to select a brain tumor image
file_path = filedialog.askopenfilename(title='Select Brain Tumor Image', filetypes=(('JPEG files', '*.jpg'), ('PNG files', '*.png'), ('All files', '*.*')))

# Load the selected image using OpenCV
if file_path:
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    def threshold_comparison(image):
        # Apply Otsu's thresholding
        start = time.time()
        _, otsu_thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        otsu_time = time.time() - start

        # Apply adaptive thresholding
        start = time.time()
        adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        adaptive_time = time.time() - start

        # Apply simple thresholding
        start = time.time()
        _, simple_thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        simple_time = time.time() - start

        # Apply binary thresholding
        start = time.time()
        _, binary_thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
        binary_time = time.time() - start

        # Compare the results
        otsu_count = cv2.countNonZero(otsu_thresh)
        adaptive_count = cv2.countNonZero(adaptive_thresh)
        simple_count = cv2.countNonZero(simple_thresh)
        binary_count = cv2.countNonZero(binary_thresh)

        times = {
            "Otsu": otsu_time,
            "Adaptive": adaptive_time,
            "Simple": simple_time,
            "Binary": binary_time
        }

        counts = {
            "Otsu": otsu_count,
            "Adaptive": adaptive_count,
            "Simple": simple_count,
            "Binary": binary_count
        }

        best_method = max(counts, key=counts.get)
        print(f"{best_method} thresholding produced the best result with a count of {counts[best_method]} and took {times[best_method]} seconds")

        return {
            "Otsu": otsu_thresh,
            "Adaptive": adaptive_thresh,
            "Simple": simple_thresh,
            "Binary": binary_thresh
        }

    # Perform threshold comparison
    threshold_results = threshold_comparison(image)

    # Display the thresholded images
    cv2.imshow("Otsu Thresholding", threshold_results["Otsu"])
    cv2.imshow("Adaptive Thresholding", threshold_results["Adaptive"])
    cv2.imshow("Simple Thresholding", threshold_results["Simple"])
    cv2.imshow("Binary Thresholding", threshold_results["Binary"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No file selected")    
