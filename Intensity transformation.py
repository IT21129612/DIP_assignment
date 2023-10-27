#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def adjust_intensity(image, min_intensity, max_intensity):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply contrast stretching
    stretched = cv2.normalize(gray, None, min_intensity, max_intensity, cv2.NORM_MINMAX)

    # Convert the image back to BGR color space
    result = cv2.cvtColor(stretched, cv2.COLOR_GRAY2BGR)

    return result

def open_image():
    # Prompt the user to select an image file
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])

    # Load the selected image
    image = cv2.imread(image_path)
    
    # Convert the image to RGB format for display in tkinter
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Display the original image in a new window
    #cv2.imshow('Original Image', image)

    # Prompt the user to enter the intensity levels
    #min_intensity = int(input_min.get())
    #max_intensity = int(input_max.get())

    # Adjust the intensity levels
    min_intensity = int(input_min.get())
    max_intensity = int(input_max.get())
    adjusted_image = adjust_intensity(image, min_intensity, max_intensity)

    # Convert the adjusted image to RGB format for display in tkinter
    adjusted_image_rgb = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)

    # Create PIL ImageTk objects for display in tkinter
    original_img = ImageTk.PhotoImage(Image.fromarray(image_rgb))
    adjusted_img = ImageTk.PhotoImage(Image.fromarray(adjusted_image_rgb))

    # Update the image labels
    label_original.configure(image=original_img)
    label_adjusted.configure(image=adjusted_img)
    label_original.image = original_img
    label_adjusted.image = adjusted_img
    
    # Display the adjusted image in a new window
    #cv2.imshow('Adjusted Image', adjusted_image)

def close_windows():
    cv2.destroyAllWindows()
    root.destroy()

# Create the main tkinter window
root = tk.Tk()
root.title("Image Intensity Adjustment")

# Create labels and entry fields for intensity levels
label_min = tk.Label(root, text="Minimum Intensity Level (0-255):")
label_min.pack()
input_min = tk.Entry(root)
input_min.pack()

label_max = tk.Label(root, text="Maximum Intensity Level (0-255):")
label_max.pack()
input_max = tk.Entry(root)
input_max.pack()

# Create labels for image display
label_original = tk.Label(root)
label_original.pack()

label_adjusted = tk.Label(root)
label_adjusted.pack()

# Create buttons for opening and closing windows
button_open = tk.Button(root, text="Open Image", command=open_image)
button_open.pack()

button_close = tk.Button(root, text="Close Windows", command=close_windows)
button_close.pack()

# Start the tkinter event loop
root.mainloop()
    

# Load the image
#image = cv2.imread('C:\Users\ASUS\Pictures\Saved Pictures\girl.jpg')
#image_path = input("Enter the path to the image file: ")
#min_intensity = int(input("Enter the minimum intensity level (0-255): "))
#max_intensity = int(input("Enter the maximum intensity level (0-255): "))

# Adjust the intensity levels
#adjusted_image = adjust_intensity(image, 0, 255)
#adjusted_image = adjust_intensity(image, min_intensity, max_intensity)

# Display the result
#cv2.imshow('Original Image', image)
#cv2.imshow('Adjusted Image', adjusted_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


# In[ ]:




