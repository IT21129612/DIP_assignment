#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install numpy pillow matplotlib tensorflow


# In[45]:


import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# Generate some example data (you should replace this with your own dataset)
# X_train: Noisy images
# y_train: Corresponding enhanced (clean) images
# Make sure to load and preprocess your dataset accordingly

X_train = np.random.rand(100, 256, 256, 3)  # Example noisy images
y_train = np.random.rand(100, 256, 256, 3)  # Example enhanced images

# Define your model
model = keras.Sequential()
model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=(256, 256, 3))
model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(3, (3, 3), activation='relu', padding='same'))  # Use 'relu' for final layer

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')  # Use 'mean_squared_error' loss

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Save the trained model
model.save('image_enhancement_model.h5')


# In[7]:


model.save('image_enhancement_model.keras')


# In[8]:


model.save('my_model.keras')


# In[ ]:


import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

class ImageEnhancerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Enhancer")
        self.model = load_model('image_enhancement_model.keras')
        self.target_resolution = (600, 480)

        self.create_widgets()

    def create_widgets(self):
        # Upload Button
        self.upload_button = tk.Button(self.master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        # Enhance Button
        self.enhance_button = tk.Button(self.master, text="Enhance Image", command=self.enhance_image)
        self.enhance_button.pack()

        # Original Image Label
        self.original_label = tk.Label(self.master)
        self.original_label.pack()

        # Enhanced Image Label
        self.enhanced_label = tk.Label(self.master)
        self.enhanced_label.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            original_image = Image.open(file_path)
            self.original_image = self.resize_image(original_image, self.target_resolution)
            self.show_image(self.original_image, self.original_label)

    def resize_image(self, image, target_resolution):
        return image.resize(target_resolution, Image.LANCZOS)


    def enhance_image(self):
        if hasattr(self, 'original_image'):
            # Preprocess the image
            image = self.original_image.resize((256, 256))
            image_array = np.array(image) / 255.0
            image_array = image_array.reshape((1, 256, 256, 3))
            # Enhance the image using the model
            enhanced_image_array = self.model.predict(image_array)
            enhanced_image = Image.fromarray((enhanced_image_array[0] * 255).astype(np.uint8))
            # Display the enhanced image
            self.show_image(enhanced_image, self.enhanced_label)

    def show_image(self, image, label):
        image = ImageTk.PhotoImage(image)
        label.image = image
        label.configure(image=image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEnhancerApp(root)
    root.mainloop()


# In[ ]:





# In[ ]:




