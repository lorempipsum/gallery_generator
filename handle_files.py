# Locate, copy, compress files. 


import os 
import glob
import shutil
from PIL import Image, ImageDraw, ImageFont

EXTENSIONS = ['.jpg', '.jpeg', '.png']
WATERMARK = '© Sander Lootus    www.sandroid.dev'

# Max width and height to resize images to
MAX_WIDTH = 1800
MAX_HEIGHT = 1013

def copy_images(src_dir, dst_dir):
    """Copy images from the original directory to the gallery directory.
    """
    print(f" Finding images in {src_dir} to copy to {dst_dir}")
    for extension in EXTENSIONS:
        print(f"extension is {extension}")
        image_path = os.path.join(src_dir, '*' + extension)
        print(f"Path is {image_path}")
        for image_file in glob.iglob(image_path):
            print()
            process_image(image_file, dst_dir)

def process_image(image_path, destination_directory): 
    '''Resize and watermark the image.
    '''
    filename = os.path.basename(image_path)
    image_title, extension = os.path.splitext(filename)
    new_filename = image_title + '-resized' + extension
    destination = os.path.join(destination_directory, new_filename)


    im = Image.open(image_path).convert("RGBA")

    width, height = calculate_dimensions(im)

    im = im.resize((width, height), Image.ANTIALIAS)
    im = watermark_image(im, WATERMARK).convert('RGB')

    im.save(destination)

    print(f"Processed image {image_title} \n from: {image_path} \n to: {destination} \n")



def calculate_dimensions(im): 
    image_width, image_height = im.size

    if image_width > 1800: 
        width_factor = 1800 / image_width
    else: 
        # Don't upscale
        width_factor = 1 

    if image_height > 1013: 
        height_factor = 1013 / image_height
    else:
        height_factor = 1 

    resize_factor = min(width_factor, height_factor)

    return int(image_width * resize_factor), int(image_height * resize_factor)

def watermark_image(im, watermark_text): 
    width, height = im.size

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', im.size, (255,255,255,0))

    # get a font
    font = ImageFont.truetype('arial.ttf', 20)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    x = width
    y = height

    d.text((40, y-40), watermark_text, fill=(255, 255, 255, 100), font=font)
    combined = Image.alpha_composite(im, txt)    
    return combined

