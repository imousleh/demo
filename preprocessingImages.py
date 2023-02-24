import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import cv2

def resize_images(folder_path):
    if folder_path:
        # Get a list of image files in the selected folder
        image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG') or f.endswith('.jpeg')]

        # Resize and crop each image and save it in the same folder with "_resized" appended to the filename
        for image_file in image_files:
            # Open the original image and resize it
            original_image_path = os.path.join(folder_path, image_file)
            original_image = Image.open(original_image_path)
            resized_image = original_image.resize((280, 280))

            # Crop the image by 12 pixels from the edges
            width, height = resized_image.size
            left = 12
            top = 12
            right = width - 12
            bottom = height - 12
            resized_image = resized_image.crop((left, top, right, bottom))

            # Convert the image to grayscale mode
            resized_image = resized_image.convert('L')

            # Save the resized image with 300 dpi resolution
            resized_image_path = os.path.join(folder_path, image_file.split('.')[0] + '_resized.' + image_file.split('.')[1])
            resized_image.save(resized_image_path, dpi=(300, 300))

            # Delete the original image
            os.remove(original_image_path)

        # Show a message box to indicate success
        message = f"All images in {folder_path} have been resized and cropped."
        messagebox.showinfo("Resize Images", message)

def select_folder():
    # Open a dialog box to select a folder and call the resize_images function
    folder_path = filedialog.askdirectory()
    resize_images(folder_path)

# Create a GUI with a button to select a folder
root = Tk()
root.title("Image Resizer")
root.geometry("300x100")

button = Button(root, text="Select Folder", command=select_folder)
button.pack(pady=20)

root.mainloop()
