from PIL import Image
import numpy as np
import os

def compare_images(image1, image2):
    # Load the images
    img1 = Image.open(image1)
    img2 = Image.open(image2)

    # Convert the images to grayscale
    gray1 = img1.convert('L')
    gray2 = img2.convert('L')

    # Convert the images to numpy arrays
    arr1 = np.array(gray1)
    arr2 = np.array(gray2)

    # Calculate the absolute difference between the images
    diff = np.abs(arr1 - arr2)

    # Calculate the threshold to determine the different pixels
    threshold = 30

    # Create a mask of the different pixels
    mask = diff > threshold

    # Count the number of different pixels
    diff_pixels = np.sum(mask)

    # Calculate the percentage of difference between the images
    total_pixels = arr1.shape[0] * arr1.shape[1]
    diff_percentage = (diff_pixels / total_pixels) * 100

    return diff_percentage

def change_image_name(image, new_name):
    # Obtener la ruta del directorio de la imagen
    image_dir = os.path.dirname(image)
    
    # Obtener la extensión de la imagen
    image_ext = os.path.splitext(image)[1]
    
    # Construir el nuevo nombre de la imagen
    new_image_name = new_name + image_ext
    
    # Construir la nueva ruta de la imagen
    new_image_path = os.path.join(image_dir, new_image_name)
    
    # Cambiar el nombre de la imagen
    os.rename(image, new_image_path)
    
    return new_image_path

def move_image(image, new_path):
    # Mover la imagen a una nueva ubicación
    import shutil
    shutil.move(image, new_path)

def delete_image(image):
    # Eliminar la imagen
    os.remove(image)

def color_pixel(image_path, x, y):
    image = Image.open(image_path)
    pixel = image.getpixel((x, y))
    return pixel
