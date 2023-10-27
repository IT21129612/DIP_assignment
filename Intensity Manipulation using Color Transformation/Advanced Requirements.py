#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import necessary libraries
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

# Create the main window
root = Tk()
root.title("Image Processing App")
root.geometry('1200x600')

# Global variable to store original image
original_image = None

# Function to open and display the image file
def open_image():
    global original_image
    file_path = filedialog.askopenfilename()
    # Open the image using OpenCV
    img = cv2.imread(file_path)
    # Store original image for reference
    original_image = img.copy()
    # Resize the image
    img = cv2.resize(img, (500, 400))
    # Convert the image from BGR to RGB format
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Convert the image for Tkinter
    img = ImageTk.PhotoImage(Image.fromarray(img))
    # Update the original image panel
    original_img_panel.configure(image=img)
    original_img_panel.image = img

# Function for histogram equalization
def histogram_equalization():
    global original_image
    # Check if an image is present
    if original_image is None:
        messagebox.showerror("Error", "Please upload an image before applying modifications.")
        return
    # Convert image to grayscale
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # Apply histogram equalization
    img = cv2.equalizeHist(gray_image)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img = cv2.resize(img, (500, 400))
    img = ImageTk.PhotoImage(Image.fromarray(img))
    processed_img_panel.configure(image=img)
    processed_img_panel.image = img

# Function for gamma correction
def gamma_correction():
    global original_image
    # Check if an image is present
    if original_image is None:
        messagebox.showerror("Error", "Please upload an image before applying modifications.")
        return
    # Ask for gamma value
    gamma = simpledialog.askfloat("Input", "Gamma value?", minvalue=0.1, maxvalue=5.0)
    # Apply gamma correction
    img = cv2.pow(original_image/255., gamma)
    # Convert the image depth back to CV_8U and normalize values to range [0, 255]
    img = np.clip(img*255, 0, 255).astype('uint8')
    img = cv2.resize(img, (500, 400))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img))
    processed_img_panel.configure(image=img)
    processed_img_panel.image = img

# Function to adjust temperature
def adjust_temperature():
    global original_image
    # Check if an image is present
    if original_image is None:
        messagebox.showerror("Error", "Please upload an image before applying modifications.")
        return
    # Ask for temperature
    temperature = simpledialog.askinteger("Input", "Temperature value? (-100 to 100)", minvalue=-100, maxvalue=100)
    temperature = temperature / 100.0
    blue, green, red = cv2.split(original_image)
    # increasing the blue channel gives a cooler effect
    # increasing yellow (subtracting blue from all channels and adding green to green channel) gives a warmer effect
    if temperature <= 0:
        # increase "coolness" by adding to blue channel
        blue = blue + abs(temperature) * 128
    else:
        # increase "warmth" by adding to all channels (yellow effect)
        red = red + temperature * 128
        green = green + temperature * 128
        blue = blue - temperature * 128
    blue = cv2.convertScaleAbs(blue)
    green = cv2.convertScaleAbs(green)
    red = cv2.convertScaleAbs(red)
    img = cv2.merge((blue, green, red))
    img = cv2.resize(img, (500, 400))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img))
    processed_img_panel.configure(image=img)
    processed_img_panel.image = img

# Function to adjust tint
def adjust_tint():
    global original_image
    # Check if an image is present
    if original_image is None:
        messagebox.showerror("Error", "Please upload an image before applying modifications.")
        return
    # Ask for tint
    tint = simpledialog.askinteger("Input", "Tint value? (-100 to 100)", minvalue=-100, maxvalue=100)
    tint = tint / 100.0
    blue, green, red = cv2.split(original_image)
    # increasing the green channel gives more green tint
    # increasing magenta can be done by adding to red and blue channels (since magenta is actually a blend of red and blue)
    if tint <= 0:
        # adjust for more green tint by adding to green channel
        green = green + abs(tint) * 128
    else:
        # adjust for more magenta tint by adding to red and blue channels
        red = red + tint * 128
        blue = blue + tint * 128
    blue = cv2.convertScaleAbs(blue)
    green = cv2.convertScaleAbs(green)
    red = cv2.convertScaleAbs(red)
    img = cv2.merge((blue, green, red))
    img = cv2.resize(img, (500, 400))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img))
    processed_img_panel.configure(image=img)
    processed_img_panel.image = img

# Function to adjust white balance
def white_balance():
    global original_image
    # Check if an image is present
    if original_image is None:
        messagebox.showerror("Error", "Please upload an image before applying modifications.")
        return
    # Compute per-channel means (averages)
    blue, green, red = cv2.split(original_image)
    # Compute the average of the averages (this will give us the overall average color of the image assuming it should be gray)
    avg = (np.average(blue) + np.average(green) + np.average(red)) / 3
    # Scale each channel to make the average color of our image equal to the overall average (gray)
    blue = cv2.convertScaleAbs(blue * (avg / np.average(blue)))
    green = cv2.convertScaleAbs(green * (avg / np.average(green)))
    red = cv2.convertScaleAbs(red * (avg / np.average(red)))
    # Merge the channels back together
    img = cv2.merge((blue, green, red))
    img = cv2.resize(img, (500, 400))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img))
    processed_img_panel.configure(image=img)
    processed_img_panel.image = img

# Function to adjust saturation
def adjust_saturation():
    global original_image
    # Check if an image is present
    if original_image is None:
        messagebox.showerror("Error", "Please upload an image before applying modifications.")
        return
    # Ask for saturation adjustment value
    sat_value = simpledialog.askfloat("Input", "Saturation adjustment value (-100 to 100)?", minvalue=-100.0, maxvalue=100.0)
    # Scale saturation value to OpenCV's scale
    sat_value = sat_value * 2.55
    img = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    v = img[:, :, 1]
    v = np.where(v <= 255 - sat_value, v + sat_value, 255)
    img[:, :, 1] = v
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    img = cv2.resize(img, (500, 400))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img))
    processed_img_panel.configure(image=img)
    processed_img_panel.image = img
    
# Function to reset the application
def reset_application():
    global original_image
    original_image = None
    blank = ImageTk.PhotoImage(Image.new('RGB', (500, 400)))
    original_img_panel.configure(image=blank)
    original_img_panel.image = blank
    processed_img_panel.configure(image=blank)
    processed_img_panel.image = blank

# Button to open an image file
open_button = Button(root, text="Open Image", command=open_image)
open_button.pack()

# Button to reset the application
reset_button = Button(root, text="Reset Application", command=reset_application)
reset_button.pack()

# Menu button for tonal transformations
tonal_menu = Menubutton(root, text="Tonal Transformations", relief=RAISED)
tonal_menu.pack()
tonal_menu.menu = Menu(tonal_menu, tearoff=0)
tonal_menu["menu"] = tonal_menu.menu
tonal_menu.menu.add_command(label="Histogram Equalization", command=histogram_equalization)
tonal_menu.menu.add_command(label="Gamma Correction", command=gamma_correction)

# Menu button for color balancing
color_menu = Menubutton(root, text="Color Balancing", relief=RAISED)
color_menu.pack()
color_menu.menu = Menu(color_menu, tearoff=0)
color_menu["menu"] = color_menu.menu
color_menu.menu.add_command(label="Adjust temperature", command=adjust_temperature)
color_menu.menu.add_command(label="Adjust tint", command=adjust_tint)

# Menu button for color correction
color_correction_menu = Menubutton(root, text="Color Correction", relief=RAISED)
color_correction_menu.pack()
color_correction_menu.menu = Menu(color_correction_menu, tearoff=0)
color_correction_menu["menu"] = color_correction_menu.menu
color_correction_menu.menu.add_command(label="White Balance Adjustments", command=white_balance)
color_correction_menu.menu.add_command(label="Saturation Adjustments", command=adjust_saturation)


# Create a frame to contain the original and processed images
image_frame = Frame(root)
image_frame.pack()

# Create a panel to display the original image
original_img_panel = Label(image_frame)
original_img_panel.grid(row=0, column=0)

# Create a panel to display the processed image
processed_img_panel = Label(image_frame)
processed_img_panel.grid(row=0, column=1)



root.mainloop()


# In[ ]:




