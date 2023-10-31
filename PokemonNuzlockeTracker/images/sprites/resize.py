from PIL import Image
import os
import time

def resize_image(input_path, output_path, size=(64, 64)):
    # Open the image using Pillow
    img = Image.open(input_path)

    # Convert to RGBA if not already in that format (for images with transparency)
    img = img.convert("RGBA")

    # Find the bounding box of the non-transparent pixels
    bbox = img.getbbox()

    # Crop the image to the bounding box to remove the whitespace
    img_cropped = img.crop(bbox)

    # Resize the cropped image to the desired size
    #img_resized = img_cropped.resize(size, Image.Resampling.LANCZOS)

    # Save the resized image
    print(f"saving to: {output_path}")
    img_cropped.save(output_path)

# Example usage
oldfilepath = os.path.join(os.getcwd(), "PokemonNuzlockeTracker", "images", "sprites", "pokemon")
newFilePath = os.path.join(os.getcwd(), "PokemonNuzlockeTracker", "images", "sprites", "pokemonMinimalWhitespace")
oldfiles = [f for f in os.listdir(oldfilepath) if f.lower().endswith('.png')]
for index, file in enumerate(oldfiles):
    try:
        resize_image(os.path.join(oldfilepath, file), os.path.join(newFilePath, file))
    except:
        print(file, "exception")
        time.sleep(0.5)
        continue




# input_image_path = os.path.join(os.getcwd(), "PokemonNuzlockeTracker", "images", "sprites", "pokemon", "aerodactyl.png") # Replace with your image path
# print(input_image_path)
# output_image_path = os.path.join(os.getcwd(), "PokemonNuzlockeTracker", "images", "sprites", "pokemonMinimalWhitespace", "aerodactyl.png") # Replace with the desired output path
# resize_image(input_image_path, output_image_path)
