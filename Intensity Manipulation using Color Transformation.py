#!/usr/bin/env python
# coding: utf-8

# In[4]:


import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Define the intensity transformation function
def intensity_transform(image, gamma):
    # Apply gamma correction to the image
    gamma_corrected_image = cv2.pow(image/255.0, gamma)
    gamma_corrected_image = (gamma_corrected_image*255).astype('uint8')
    
    return gamma_corrected_image

# Define the tonal transformation function
def tonal_transform(image, contrast, brightness):
    # Apply contrast and brightness adjustment to the image
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    
    return adjusted_image

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

# Define the function to perform image processing and update the image
def process_image():
    # Ask the user to select an image file using file dialog
    image_path = filedialog.askopenfilename()
    
    # Check if the user selected a file
    if image_path:
        # Load the image
        image = cv2.imread(image_path)
        
        # Get the intensity transformation values from the entry widgets
        gamma = float(gamma_entry.get())
        
        # Get the tonal transformation values from the entry widgets
        contrast = float(contrast_entry.get())
        brightness = int(brightness_entry.get())
        
        # Get the color balancing values from the entry widgets
        red_scale = float(red_entry.get())
        green_scale = float(green_entry.get())
        blue_scale = float(blue_entry.get())
        
        # Apply intensity transformation to the image
        intensity_transformed_image = intensity_transform(image, gamma)
        
        # Apply tonal transformation to the image
        tonal_transformed_image = tonal_transform(intensity_transformed_image, contrast, brightness)
        
        # Apply color balancing to the image
        balanced_image = color_balance(tonal_transformed_image, red_scale, green_scale, blue_scale)
        
        # Convert the images to PIL format for displaying in Tkinter
        original_image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        processed_image_pil = Image.fromarray(cv2.cvtColor(balanced_image, cv2.COLOR_BGR2RGB))

        # Create Tkinter PhotoImage objects from the PIL images
        original_image_tk = ImageTk.PhotoImage(original_image_pil)
        processed_image_tk = ImageTk.PhotoImage(processed_image_pil)

        # Update the image labels with the original and processed images
        original_image_label.configure(image=original_image_tk)
        original_image_label.image = original_image_tk
        processed_image_label.configure(image=processed_image_tk)
        processed_image_label.image = processed_image_tk

# Create the Tkinter window
window = tk.Tk()

# Create the original image label
original_image_label = tk.Label(window)

# Create the processed image label
processed_image_label = tk.Label(window)

# Create the button for selecting the image file and applying image processing
select_image_button = tk.Button(window, text="Select Image", command=process_image)

# Create the entries for intensity transformation input
gamma_entry = tk.Entry(window)
gamma_entry.insert(tk.END, '1.0')  # Set a default value

# Create the entries for tonal transformation input
contrast_entry = tk.Entry(window)
contrast_entry.insert(tk.END, '1.0')  # Set a default value
brightness_entry = tk.Entry(window)
brightness_entry.insert(tk.END, '0')  # Set a default value

# Create the entries for color balancing input
red_entry = tk.Entry(window)
red_entry.insert(tk.END, '1.0')  # Set a default value
green_entry = tk.Entry(window)
green_entry.insert(tk.END, '1.0')  # Set a default value
blue_entry = tk.Entry(window)
blue_entry.insert(tk.END, '1.0')  # Set a default value

# Create the labels for intensity transformation input
gamma_label = tk.Label(window, text="Gamma:")

# Create the labels for tonal transformation input
contrast_label = tk.Label(window, text="Contrast:")
brightness_label = tk.Label(window, text="Brightness:")

# Create the labels for color balancing input
red_label = tk.Label(window, text="Red Scale:")
green_label = tk.Label(window, text="Green Scale:")
blue_label = tk.Label(window, text="Blue Scale:")

# Pack the image labels, buttons, and entries into the window
original_image_label.pack(side=tk.LEFT, padx=10, pady=10)
processed_image_label.pack(side=tk.RIGHT, padx=10, pady=10)
select_image_button.pack()
gamma_label.pack()
gamma_entry.pack()
contrast_label.pack()
contrast_entry.pack()
brightness_label.pack()
brightness_entry.pack()
red_label.pack()
red_entry.pack()
green_label.pack()
green_entry.pack()
blue_label.pack()
blue_entry.pack()

# Run the Tkinter event loop
window.mainloop()


# In[ ]:




