# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 09:33:57 2021

@author: PAORAIN
"""

import cv2 as cv
import glob

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
    tmp = cv.imread(path, cv.IMREAD_UNCHANGED)
    h, w = tmp.shape[:2]
    long.append(w)
    haut.append(h)
    return tmp, long, haut

def recadrage(T):
    """
    Récadre les images en fonction des pixels noirs.

    Parameters:
    T (list): Liste des images.

    Returns:
    int: Nombre de pixels à gauche.
    int: Nombre de pixels à droite.
    int: Nombre de pixels en haut.
    int: Nombre de pixels en bas.
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
            if image[i, h // 2] == 0:
                pixels_left += 1
                i += 1
            else:
                break

        for i in range(1, w):
            if image[-i, h // 2] == 0:
                pixels_right += 1
                i += 1
            else:
                break

        for j in range(h):
            if image[w // 2, j] == 0:
                pixels_top += 1
                j += 1
            else:
                break

        for j in range(1, h):
            if image[w // 2, -j] == 0:
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
    Redimensionne les images à une taille commune.

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
        s = (mh, ml)
        for path in images:
            img = cv.imread(path)
            if img is None:
                continue
            res = cv.resize(img, s, interpolation=cv.INTER_CUBIC)
            cv.imwrite(path, res)

def align_img(images):
    """
    Aligne les images.

    Parameters:
    images (list): Liste des chemins des images.
    """
    I = []
    T = []
    print("Aligning images ... ")
    for path in images:
        print(path)
        img = cv.imread(path, cv.IMREAD_UNCHANGED)
        I.append(img)

    if I:
        alignMTB = cv.createAlignMTB()
        alignMTB.process(I, I)
        cpt = 0

        for image in I:
            img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            cv.imwrite(images[cpt], img)
            T.append(img)
            cpt += 1

        i = 0
        l, r, t, b = recadrage(T)
        for image in T:
            w, h = image.shape
            res = image[l:w - r, t:h - b]
            cv.imwrite(images[i], res)
            i += 1

def mediane(images, kernel):
    """
    Applique un filtre médian aux images.

    Parameters:
    images (list): Liste des chemins des images.
    kernel (int): Taille du noyau du filtre médian.
    """
    for path in images:
        print("ok")
        img = cv.imread(path)
        img_2 = cv.medianBlur(img,kernel)
        cv.imwrite(path,img_2)

    


##### main #####

def main(path,test = False,flou = None):

    """
    Entrez le chemin absolue du dossier dans lequel 
    se trouve les images, suivie de /*/*.tif
    """

    if test:

        images = glob.glob(path+ "/*.tif")
        if flou is not None:
            mediane(images,flou)
        print(images)
        resize_images_to_common_dimensions(images)
        align_img(images)        

        return 0
    files = glob.glob(path)

    for file in files:
        images = glob.glob(file+"/*.tif")          
        resize_images_to_common_dimensions(images)
        align_img(images)

if __name__ == "__main__" : 
    main("C:/Users/AHUMEAU/Desktop/donnees_triees/panoramas",test = True)
