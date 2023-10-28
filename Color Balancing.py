#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Define the color balancing function
def color_balance(image, red_scale, green_scale, blue_scale):
    # Split the image into its color channels
    b, g, r = cv2.split(image)
    
    # Apply color scaling to each channel
    b = cv2.multiply(b, blue_scale)
    g = cv2.multiply(g, green_scale)
    r = cv2.multiply(r, red_scale)
    
    # Merge the color channels back into a single image
    balanced_image = cv2.merge((b, g, r))
    
    return balanced_image

# Define the function to perform color balancing and update the image
def perform_color_balancing():
    # Ask the user to select an image file using file dialog
    image_path = filedialog.askopenfilename()
    
    # Check if the user selected a file
    if image_path:
        # Load the image
        image = cv2.imread(image_path)
        
        # Get the color scaling values from the entry widgets
        red_scale = float(red_entry.get())
        green_scale = float(green_entry.get())
        blue_scale = float(blue_entry.get())
        
        # Apply color balancing to the image
        balanced_image = color_balance(image, red_scale, green_scale, blue_scale)
        
        # Convert the images to PIL format for displaying in Tkinter
        original_image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        balanced_image_pil = Image.fromarray(cv2.cvtColor(balanced_image, cv2.COLOR_BGR2RGB))

        # Create Tkinter PhotoImage objects from the PIL images
        original_image_tk = ImageTk.PhotoImage(original_image_pil)
        balanced_image_tk = ImageTk.PhotoImage(balanced_image_pil)

        # Update the image labels with the original and balanced images
        original_image_label.configure(image=original_image_tk)
        original_image_label.image = original_image_tk
        balanced_image_label.configure(image=balanced_image_tk)
        balanced_image_label.image = balanced_image_tk

# Create the Tkinter window
window = tk.Tk()

# Create the original image label
original_image_label = tk.Label(window)

# Create the balanced image label
balanced_image_label = tk.Label(window)

# Create the button for selecting the image file and applying color balancing
select_image_button = tk.Button(window, text="Select Image", command=perform_color_balancing)

# Create the entries for color scaling input
red_entry = tk.Entry(window)
red_entry.insert(tk.END, '1.0')  # Set a default value
green_entry = tk.Entry(window)
green_entry.insert(tk.END, '1.0')  # Set a default value
blue_entry = tk.Entry(window)
blue_entry.insert(tk.END, '1.0')  # Set a default value

# Create the labels for color scaling input
red_label = tk.Label(window, text="Red Scale:")
green_label = tk.Label(window, text="Green Scale:")
blue_label = tk.Label(window, text="Blue Scale:")

# Pack the image labels, buttons, and entries into the window
original_image_label.pack(side=tk.LEFT, padx=10, pady=10)
balanced_image_label.pack(side=tk.RIGHT, padx=10, pady=10)
select_image_button.pack()
red_label.pack()
red_entry.pack()
green_label.pack()
green_entry.pack()
blue_label.pack()
blue_entry.pack()

# Run the Tkinter event loop
window.mainloop()

