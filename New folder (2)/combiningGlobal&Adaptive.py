import cv2
import tkinter as tk
from tkinter import filedialog


def select_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='Select Image', filetypes=(('JPEG files', '*.jpg'), ('PNG files', '*.png'), ('All files', '*.*')))
    if file_path:
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        cv2.imshow("Original Image", image)
        return image
    else:
        return None


def threshold_segmentation(image):
    # Apply Otsu's thresholding
    _, otsu_thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Apply adaptive thresholding
    adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Combine the results
    combined_thresh = cv2.bitwise_or(otsu_thresh, adaptive_thresh)

    # Show the results
    cv2.imshow("Combined Thresholding", combined_thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    image = select_image()
    if image is not None:
        threshold_segmentation(image)
