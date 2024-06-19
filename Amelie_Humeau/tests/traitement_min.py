import cv2
import os
import glob
import numpy as np
from PIL import Image


def Openimage(path):
    '''
    Fonction qui prend en argument le chemin d'une image
    et qui renvoie le chemin absolu ainsi que la matrice
    qui représente l'image
    '''
    tmp = Image.open(path)
    img = np.array(tmp)
    tmp.close()
    return img
def convert12to8(img):
    print("Conversion")
    """
    Fonction qui prend en argument une matrice représentant une
    image et qui renvoie une matrice qui représente l'image en 8 bits
    """
    minim = np.amin(img)
    maxi = np.amax(img)
    data_conv = np.array(np.rint((img - minim) / float(maxi - minim) * 255.0), dtype=np.uint8)
    return data_conv

def main(input_folder):
    print(input_folder)
    images_paths = glob.glob(input_folder + "/*/*.tif")

    for path in images_paths:
        print(path)
        img = Openimage(path)
        image_8bits = convert12to8(img)
        
        cv2.imwrite(path,image_8bits)

if __name__ == '__main__':
    img = np.array([[0,4095],[2048,1024]])
    img_8bit = convert12to8(img)
    print(img,img_8bit)
