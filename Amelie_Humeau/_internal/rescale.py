# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 09:33:57 2021

@author: PAORAIN
"""

import cv2 as cv
import glob
from PIL import Image
import numpy as np
def Openimage(path, long=[], haut=[]):
    """
    Ouvre une image et retourne l'image, la longueur et la hauteur.

    Parameters:
    path (str): Chemin de l'image.
    long (list): Liste des longueurs des images.
    haut (list): Liste des hauteurs des images.

    Returns:
    numpy.ndarray: Image ouverte.
    list: Liste des longueurs des images.
    list: Liste des hauteurs des images.
    """
    tmp = Image.open(path)
    h, w = tmp.size
    long.append(w)
    haut.append(h)
    return tmp, long, haut

def recadrage(T):
    """
    Récadre les images en fonction des pixels noirs.

    Parameters:
    T (list): Liste des images.

    Returns:
    int l: Nombre de pixels à gauche.
    int r: Nombre de pixels à droite.
    int t: Nombre de pixels en haut.
    int b: Nombre de pixels en bas.
    """
    left = [0]
    right = [0]
    top = [0]
    bottom = [0]

    for image in T:
        w, h = image.shape
        pixels_left = 0
        pixels_right = 0
        pixels_top = 0
        pixels_bottom = 0

        for i in range(w):
            if image[i, h // 2] == 0 or image[i, h // 2] == 255:
                pixels_left += 1
                i += 1
            else:
                break

        for i in range(1, w):
            if image[-i, h // 2] == 0 or image[-i, h // 2] == 255  :
                pixels_right += 1
                i += 1
            else:
                break

        for j in range(h):
            if image[w // 2, j] == 0 or image[w // 2, j] == 255:
                pixels_top += 1
                j += 1
            else:
                break

        for j in range(1, h):
            if image[w // 2, -j] == 0 or image[w // 2, -j] ==255:
                pixels_bottom += 1
                j += 1
            else:
                break

        left.append(pixels_left)
        right.append(pixels_right)
        top.append(pixels_top)
        bottom.append(pixels_bottom)

    l = max(left)
    r = max(right)
    t = max(top)
    b = max(bottom)

    return l, r, t, b

def resize_images_to_common_dimensions(images):
    """
    Redimensionne les images à une taille commune en conservant le ratio.

    Parameters:
    images (list): Liste des chemins des images.
    """
    long = []
    haut = []
    I = []

    print("Resizing images ... ")
    for path in images:
        img = Openimage(path, long, haut)
        I.append(img)

    if haut and long:
        ml = min(haut)
        mh = min(long)

        for path in images:
            try:
                img = Image.open(path)
                res = np.array(img)

                if len(res.shape) == 2:  # Grayscale image with shape (height, width)
                    res = cv.cvtColor(res, cv.COLOR_GRAY2RGB)

                if res.shape[2] == 2:
                    # Assuming we want to duplicate the first channel to create a 3-channel image
                    res = cv.merge([res[:, :, 0], res[:, :, 0], res[:, :, 0]])

                # Maintain aspect ratio
                h, w = res.shape[:2]
                if w > h:
                    new_w = mh
                    new_h = int(h * (mh / w))
                else:
                    new_h = ml
                    new_w = int(w * (ml / h))

                new_size = (new_w, new_h)
                res = cv.resize(res, new_size, interpolation=cv.INTER_CUBIC)

                cv.imwrite(path, res)
                print(f"Image saved to {path}")
            
            except Exception as e:
                print(f"Error processing {path}: {e}")


def align_img(images,kernel,recadre = False):
    """
    Aligne les images.

    Parameters:
    images (list): Liste des chemins des images.
    """
    I = []
    T = []
    print("Aligning images ... ")
    
    # Read images and find minimum dimensions
    min_width, min_height = float('inf'), float('inf')
    for path in images:
        print(f"Reading image: {path}")
        img = Image.open(path)
        if img is None:
            print(f"Error: Unable to read image {path}")
            continue
        img = np.array(img)
        I.append(img)
        height, width = img.shape[:2]
        min_width = min(min_width, width)
        min_height = min(min_height, height)

    if not I:
        raise ValueError("No images were successfully read for alignment.")

    # Resize all images to the minimum dimensions
    resized_images = []
    for img in I:
        resized_img = cv.resize(img, (min_width, min_height), interpolation=cv.INTER_AREA)
        resized_images.append(resized_img)
    
    # Align images
    alignMTB = cv.createAlignMTB()
    alignMTB.process(resized_images, resized_images)
    
    cpt = 0
    for image in resized_images:
        if image is None or image.size == 0:
            print(f"Error: Processed image at index {cpt} is empty.")
            continue
        img_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        if kernel is not None:
            img_gray = cv.medianBlur(img_gray,kernel)
        cv.imwrite(images[cpt], img_gray)
        T.append(img_gray)
        cpt += 1

    if not T:
        raise ValueError("No images were successfully converted to grayscale and saved.")

    if recadre:
        l, r, t, b = recadrage(T)
        for i, image in enumerate(T):
            if image is None or image.size == 0:
                print(f"Error: Image for cropping at index {i} is empty.")
                continue
            h, w = image.shape
            res = image[l:h - r, t:w - b]
            if res is None or res.size == 0:
                print(f"Error: Cropped image at index {i} is empty.")
                continue
            cv.imwrite(images[i], res)

        

    


##### main #####

def main(path,onedir = False,flou = None,recadre=False):

    """
    Entrez le chemin absolue du dossier dans lequel 
    se trouve les images, suivie de /*/*.tif
    """

    if onedir:

        images = glob.glob(path+ "/*.tif")
        print(images)
        resize_images_to_common_dimensions(images)
        align_img(images,flou,recadre=recadre)        

        return 0
    files = glob.glob(path)
    print(files)
    for file in files:
        images = glob.glob(file+"/*.tif")
        if images:
            resize_images_to_common_dimensions(images)
            align_img(images,kernel=None,recadre=True)

if __name__ == "__main__" : 
    main("C:\\Users\\AHUMEAU\\Desktop\\test_expo\\test_10000\\orthos",onedir = True)
