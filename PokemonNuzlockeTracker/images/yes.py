import cv2
from kivy.app import App
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage

import os

class SoftenImageApp(App):
    def build(self):
        # Read the image using OpenCV
        pathToImage = os.path.join(os.getcwd(), "PokemonNuzlockeTracker", "images" , 'bg.gif')
        image = cv2.imread(pathToImage)  # Replace 'example.png' with your image filename
        print(pathToImage)

        # Apply Gaussian blur to the image
        blurred_image = cv2.GaussianBlur(image, (15, 15), 0)  # Adjust kernel size for blur strength

        # Convert OpenCV image to Kivy CoreImage
        kivy_image = CoreImage(cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB))

        # Display the blurred image in Kivy
        img = KivyImage(texture=kivy_image.texture)

        return img

if __name__ == '__main__':
    SoftenImageApp().run()

