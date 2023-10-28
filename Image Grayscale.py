#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter

class ImageProcessingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Tool")
        
        # Create buttons
        self.create_buttons()
        
        # Create labels
        self.create_labels()
        
        # Create option bars
        self.create_option_bars()
        
        # Create the grayscale entry segment
        self.create_grayscale_entry()
        
        # Create reset button
        self.create_reset_button()
        
        # Initialize the image variable
        self.image = None
        self.modified_image = None
        self.cropping = False
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_rectangle = None
    
    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.upload_button = tk.Button(button_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.grid(row=0, column=0, padx=10)
        
        self.bw_button = tk.Button(button_frame, text="Convert to Black and White", command=self.convert_to_bw)
        self.bw_button.grid(row=2, column=0, padx=10)
        
        self.grayscale_button = tk.Button(button_frame, text="Convert to Grayscale", command=self.convert_to_grayscale)
        self.grayscale_button.grid(row=3, column=0, padx=10)

        self.color_invert_button = tk.Button(button_frame, text="Color Invert (Grayscale)", command=self.color_invert)
        self.color_invert_button.grid(row=4, column=0, padx=10)

        self.sharpen_button = tk.Button(button_frame, text="Sharpen Image", command=self.sharpen_image)
        self.sharpen_button.grid(row=5, column=0, padx=10)
        
        self.crop_button = tk.Button(button_frame, text="Crop Image", command=self.toggle_cropping)
        self.crop_button.grid(row=6, column=0, padx=10)
    
    def create_labels(self):
        label_frame = tk.Frame(self.root)
        label_frame.pack(pady=10)
        
        label = tk.Label(label_frame, text="Original Image")
        label.grid(row=0, column=0, padx=10)
        
        self.original_label = tk.Canvas(label_frame, width=400, height=400)
        self.original_label.grid(row=1, column=0, padx=10)
        
        label = tk.Label(label_frame, text="Modified Image")
        label.grid(row=0, column=1, padx=10)
        
        self.modified_label = tk.Canvas(label_frame, width=400, height=400)
        self.modified_label.grid(row=1, column=1, padx=10)
        
        
    
    def create_option_bars(self):
        bar_frame = tk.Frame(self.root)
        bar_frame.pack(pady=10)
        
        flip_label = tk.Label(bar_frame, text="Flip Image:")
        flip_label.grid(row=0, column=0, padx=10)
        self.flip_var = tk.StringVar()
        flip_combo = tk.OptionMenu(bar_frame, self.flip_var, "None", "Horizontal", "Vertical")
        flip_combo.grid(row=0, column=1, padx=10)
        flip_button = tk.Button(bar_frame, text="Apply Flip", command=self.flip_image)
        flip_button.grid(row=0, column=2, padx=10)
        
        rotate_label = tk.Label(bar_frame, text="Rotate Image (degrees):")
        rotate_label.grid(row=1, column=0, padx=10)
        self.rotate_var = tk.DoubleVar()
        rotate_scale = tk.Scale(bar_frame, variable=self.rotate_var, from_=-180, to=180, orient="horizontal", length=200)
        rotate_scale.grid(row=1, column=1, padx=10)
        rotate_button = tk.Button(bar_frame, text="Apply Rotation", command=self.rotate_image)
        rotate_button.grid(row=1, column=2, padx=10)
    
    def create_reset_button(self):
        reset_button = tk.Button(self.root, text="Reset", command=self.reset_image)
        reset_button.pack(pady=10)
    
    def create_grayscale_entry(self):
        grayscale_frame = tk.Frame(self.root)
        grayscale_frame.pack(pady=10)
        
        grayscale_label = tk.Label(grayscale_frame, text="Set Grayscale Value (0-255):")
        grayscale_label.grid(row=0, column=0, padx=10)
        
        self.grayscale_var = tk.IntVar()
        self.grayscale_entry = tk.Entry(grayscale_frame, textvariable=self.grayscale_var)
        self.grayscale_entry.grid(row=0, column=1, padx=10)
        
        apply_grayscale_button = tk.Button(grayscale_frame, text="Apply Grayscale", command=self.apply_grayscale)
        apply_grayscale_button.grid(row=0, column=2, padx=10)
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image = Image.open(file_path)
            self.modified_image = self.image.copy()
            self.show_image(self.image, self.original_label)
            self.show_image(self.modified_image, self.modified_label)
    
    def show_image(self, image, label):
        image_resized = image.resize((400, 400))
        image_tk = ImageTk.PhotoImage(image_resized)
        label.image = image_tk
        label.create_image(0, 0, anchor='nw', image=image_tk)
    
    def convert_to_bw(self):
        if self.image:
            self.modified_image = self.image.convert("1")
            self.show_image(self.modified_image, self.modified_label)
    
    def convert_to_grayscale(self):
        if self.image:
            self.modified_image = self.image.convert("L")
            self.show_image(self.modified_image, self.modified_label)
    
    def apply_grayscale(self):
        if self.image:
            grayscale_value = self.grayscale_var.get()
            self.modified_image = Image.eval(self.modified_image, lambda x: x + grayscale_value)
            self.show_image(self.modified_image, self.modified_label)
            self.update_grayscale_label()
            
    def update_grayscale_label(self):
        grayscale_value = self.grayscale_var.get()
        self.grayscale_label.config(text=f"Grayscale Value: {grayscale_value}")
        
    
    def color_invert(self):
        if self.image and self.modified_image.mode == 'L':
            inverted_data = [255 - pixel for pixel in self.modified_image.getdata()]
            self.modified_image.putdata(inverted_data)
            self.show_image(self.modified_image, self.modified_label)

    def sharpen_image(self):
        if self.image:
            self.modified_image = self.modified_image.filter(ImageFilter.SHARPEN)
            self.show_image(self.modified_image, self.modified_label)
    
    def toggle_cropping(self):
        if self.image:
            self.cropping = not self.cropping
            if self.cropping:
                self.crop_button.config(text="Confirm Crop")
                self.crop_start_x = 0
                self.crop_start_y = 0
                self.crop_rectangle = None
                self.original_label.bind("<ButtonPress-1>", self.start_cropping)
                self.original_label.bind("<B1-Motion>", self.update_cropping)
                self.original_label.bind("<ButtonRelease-1>", self.finish_cropping)
            else:
                self.crop_button.config(text="Crop Image")
                self.original_label.unbind("<ButtonPress-1>")
                self.original_label.unbind("<B1-Motion>")
                self.original_label.unbind("<ButtonRelease-1>")
    
    def start_cropping(self, event):
        self.crop_start_x = event.x
        self.crop_start_y = event.y
    
    def update_cropping(self, event):
        if self.crop_rectangle:
            self.original_label.delete(self.crop_rectangle)
        x, y = self.crop_start_x, self.crop_start_y
        x1, y1 = event.x, event.y
        self.crop_rectangle = self.original_label.create_rectangle(x, y, x1, y1, outline="red")
    
    def finish_cropping(self, event):
        if self.crop_rectangle:
            self.original_label.delete(self.crop_rectangle)
            x, y = self.crop_start_x, self.crop_start_y
            x1, y1 = event.x, event.y
            self.crop_rectangle = None
            self.crop_image(x, y, x1, y1)
            self.toggle_cropping()
    
    def crop_image(self, x1, y1, x2, y2):
        if self.image and x1 < x2 and y1 < y2:
            self.modified_image = self.modified_image.crop((x1, y1, x2, y2))
            self.show_image(self.modified_image, self.modified_label)
            
    def flip_image(self):
        if self.image:
            flip_direction = self.flip_var.get()
            if flip_direction == "Horizontal":
                self.modified_image = self.modified_image.transpose(Image.FLIP_LEFT_RIGHT)
            elif flip_direction == "Vertical":
                self.modified_image = self.modified_image.transpose(Image.FLIP_TOP_BOTTOM)
            self.show_image(self.modified_image, self.modified_label)
    
    def rotate_image(self):
        if self.image:
            angle = self.rotate_var.get()
            self.modified_image = self.image.rotate(angle)
            self.show_image(self.modified_image, self.modified_label)
    
    def reset_image(self):
        if self.image:
            self.modified_image = self.image.copy()
            self.show_image(self.modified_image, self.modified_label)
            


root = tk.Tk()
app = ImageProcessingTool(root)
root.mainloop()


# In[ ]:





# In[ ]:




