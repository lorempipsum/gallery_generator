# Point to a folder. [$FOLDER_NAME]
# Find all the images [.PNG, .JPG, .JPEG] and copy them to images/galleries/[$FOLDER_NAME]
# If not already present, create a new "page" in the _pages folder with the same name as the foldername
#           layout: gallery
#           title: $FOLDER_NAME
#           permalink: "/$FOLDER_NAME/"

# Create a new file called $FOLDER_NAME.yml in_galleries: 
#           ---
#           name: "illustration"
#           arts:
#           - image: "images/path/to/your/images.jpg"
#             order: "1"
#             title: ""
#             artist: ""
#             description: ""


# argument = folder path 
import os 
import glob
import shutil

EXTENSIONS = ['.jpg', '.jpeg', '.png']

def main(jekyll_site_path, images_path, category): 

    if not os.path.exists(jekyll_site_path):
        print(f"Jekyll site path {jekyll_site_path} does not exist :(")
        return False
        
    if not os.path.exists(images_path):
        print(f"Images path {images_path} does not exist :(")
        return False

    # Get gallery name from end of images_path
    gallery_name = get_gallery_name(images_path)

    # Create page .md file for gallery
    create_page(jekyll_site_path, gallery_name, category)

    # Create gallery folder 
    gallery_path = create_gallery(jekyll_site_path, gallery_name)

    # Copy images to gallery
    # TODO: Add pillow image resize in here. 
    copy_images(images_path, gallery_path)

    # Populate gallery .yml with images in gallery_path
    populate_gallery(jekyll_site_path, gallery_name, gallery_path)

def copy_images(src_dir, dst_dir):
    """Copy images from the original directory to the gallery directory.
    """
    print(f" Finding images in {src_dir} to copy to {dst_dir}")
    for extension in EXTENSIONS:
        print(f"extension is {extension}")
        image_path = os.path.join(src_dir, '*' + extension)
        print(f"Path is {image_path}")
        for image_file in glob.iglob(image_path):
            print(f"Copying image {image_file} \n from: {src_dir} \n to: {dst_dir} \n")
            shutil.copy(image_file, dst_dir)


def create_page(jekyll_site_path, gallery_name, category):
    page_path = os.path.join(jekyll_site_path, '_pages')
    
    # make new file in ./_pages/$FOLDER_NAME.md 
    f = open(os.path.join(page_path, gallery_name + '.md') ,"w+")
    f.write("---\n")
    f.write('layout: gallery\n')
    f.write('title: ' + gallery_name + '\n')
    f.write('permalink: "' + category + '/' + gallery_name + '/"' + '\n')
    f.write("---\n")
    f.close() 
    print(f"Created page {page_path}")


def create_gallery(jekyll_site_path, gallery_name):
    """Create a gallery, and return the gallery path to add images to it.

    Args:
        jekyll_site_path (str): Root path to the jekyll site.
        gallery_name(str): Name of the gallery. 

    Returns:
        str: Full path to created gallery
    """

    gallery_path = os.path.join(jekyll_site_path, 'images', 'galleries', gallery_name)

    if not os.path.exists(gallery_path):
        os.makedirs(gallery_path)

    print(f"Created gallery path {gallery_path}")

    return gallery_path


def populate_gallery(jekyll_site_path, gallery_name, gallery_path):
    image_files = []
    for extension in EXTENSIONS: 
        image_files.extend(glob.glob(os.path.join(gallery_path, '*' + extension), recursive=False))
    # make new file in ./_galleries/$FOLDER_NAME.yml 
    f = open(os.path.join(jekyll_site_path, '_galleries', gallery_name + '.yml') ,"w+")
  
    # contents: 
    f.write('---\n')
    f.write(f'name: "{gallery_name}"\n')
    f.write('arts:\n')

    artist = 'Sander Lootus'
    description = '' 
    for i in range(len(image_files)):
        image_file = image_files[i]
        image_number = i + 1
        image_title = os.path.basename(image_file).split('.')[0]
        
        # Jekyll wants relative paths 
        image_relative_path = image_file.split(jekyll_site_path + "\\")[1]

        # Jekyll wants UNIX style paths.
        image_relative_path  = image_relative_path.replace(os.sep, '/')

        f.write(f'- image: "{image_relative_path}"\n')           
        f.write(f'  order: "{image_number}"\n')             
        f.write(f'  title: "{image_title}"\n')             
        # f.write(f'  artist: "{artist}"\n')             
        # f.write(f'  description: "{description}"\n\n')
        print(f' Wrote image {image_relative_path} with title {image_title} and order {image_number}')              
    f.write('---\n')

    f.close() 


def get_gallery_name(images_path):
    gallery_name = os.path.basename(os.path.normpath(images_path)).lower()
    print(f"Got gallery name {gallery_name}")
    return gallery_name


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Automatically create galleries for a jekyll site')
    parser.add_argument('--jekyll-site-path', metavar='path', required=True,
                        help='the path to the jekyll site')
    parser.add_argument('--images-path', metavar='path', required=True,
                        help='path to folder of new images')
    parser.add_argument('--category', metavar='path', required=True,
                        help='Category of new images')
    args = parser.parse_args()
    main(jekyll_site_path=args.jekyll_site_path, images_path=args.images_path, category=args.category)