#!/usr/bin/env python
# coding: utf-8

# In[3]:


import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Define the tonal transformation function
def tonal_transform(pixel_value, brightness_increase):
    # Increase brightness by adding the specified value
    transformed_value = pixel_value + brightness_increase
    return min(transformed_value, 255)  # Ensure the value stays within the valid range of 0-255

# Define the function to perform tonal transformation and update the image
def perform_tonal_transformation():
    # Ask the user to select an image file using file dialog
    image_path = filedialog.askopenfilename()
    
    # Check if the user selected a file
    if image_path:
        # Load the image
        image = cv2.imread(image_path)
        
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Create a copy of the grayscale image for tonal transformation
        transformed_image = gray_image.copy()
        
        # Get the brightness increase value from the entry widget
        brightness_increase = int(brightness_entry.get())
        
        # Apply tonal transformation to each pixel in the image
        for i in range(transformed_image.shape[0]):
            for j in range(transformed_image.shape[1]):
                transformed_image[i, j] = tonal_transform(transformed_image[i, j], brightness_increase)
        
        # Convert the transformed image back to BGR format for display
        transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_GRAY2BGR)
        
        # Convert the images to PIL format for displaying in Tkinter
        original_image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        transformed_image_pil = Image.fromarray(cv2.cvtColor(transformed_image, cv2.COLOR_BGR2RGB))

        # Create Tkinter PhotoImage objects from the PIL images
        original_image_tk = ImageTk.PhotoImage(original_image_pil)
        transformed_image_tk = ImageTk.PhotoImage(transformed_image_pil)

        # Update the image labels with the original and transformed images
        original_image_label.configure(image=original_image_tk)
        original_image_label.image = original_image_tk
        transformed_image_label.configure(image=transformed_image_tk)
        transformed_image_label.image = transformed_image_tk

# Create the Tkinter window
window = tk.Tk()

# Create the original image label
original_image_label = tk.Label(window)

# Create the transformed image label
transformed_image_label = tk.Label(window)

# Create the button for selecting the image file and applying tonal transformation
select_image_button = tk.Button(window, text="Select Image", command=perform_tonal_transformation)

# Create the entry for user input
brightness_entry = tk.Entry(window)
brightness_entry.insert(tk.END, '0')  # Set a default value

# Create the label for brightness input
brightness_label = tk.Label(window, text="Brightness Increase:")

# Pack the image labels, buttons, and entry into the window
original_image_label.pack(side=tk.LEFT, padx=10, pady=10)
transformed_image_label.pack(side=tk.RIGHT, padx=10, pady=10)
select_image_button.pack()
brightness_label.pack()
brightness_entry.pack()

# Run the Tkinter event loop
window.mainloop()


# In[ ]:




