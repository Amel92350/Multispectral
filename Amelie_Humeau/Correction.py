import os
import numpy as np
from PIL import Image
import cv2 as cv
from collections import defaultdict
import glob

def Openimage(path):
    '''
    Fonction qui prend en argument le chemin d'une image
    et qui renvoie le chemin absolu ainsi que la matrice
    qui représente l'image
    '''
    tmp = Image.open(path)
    img = np.array(tmp)
    tmp.close()
    path_b = os.path.abspath(path)
    return img, path_b

def convert12to8(img):
    """
    Fonction qui prend en argument une matrice représentant une
    image et qui renvoie une matrice qui représente l'image en 8 bits
    """
    minim = np.amin(img)
    maxi = np.amax(img)
    data_conv = np.array(np.rint((img - minim) / float(maxi - minim) * 255.0), dtype=np.uint8)
    return data_conv

def get_file_matrice(bande):
    """
    Fonction qui crée une matrice de coefficients de distorsion et une matrice de paramètres intrinsèques
    ENTREE : une chaîne de caractères (bande) qui contient la bande dont on veut les matrices (ex : '450nm')
    SORTIE : deux matrices dans un tuple (dist, mtx)
    """
    dist = np.zeros((1, 5))
    mtx = np.zeros((3, 3))

    with open('resources/dist_v2.txt') as f_dist, open('resources/mtx.txt') as f_mtx:
        data_dist = f_dist.readlines()
        data_mtx = f_mtx.readlines()

        for i, line_name in enumerate(data_dist):
            if line_name.strip() == bande:
                for line in data_dist[i + 1:i + 6]:
                    indice1, indice2, value = line.strip().split(' ')
                    dist[int(indice1), int(indice2)] = float(value)

        for i, line_name in enumerate(data_mtx):
            if line_name.strip() == bande:
                for line in data_mtx[i + 1:i + 6]:
                    indice1, indice2, value = line.strip().split(' ')
                    mtx[int(indice1), int(indice2)] = float(value)

    return dist, mtx

def undistort_bande(img_bande, mtx, dist, roi, new_camera_mtx):
    for img, path in img_bande:
        dst = cv.undistort(img, mtx, dist, None, new_camera_mtx)
        dst = convert12to8(dst)
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        cv.imwrite(path, dst)


def main(chemin):
    """
    Entrez le chemin absolu du dossier dans lequel 
    se trouvent les images, suivi de /*/*.tif    
    """
    images = glob.glob(os.path.join(chemin, "*.tif"))
    images_dict = defaultdict(list)

    print("Tri des images")
    for path in images:
        print(path)
        img, path_b = Openimage(path)
        for wavelength in ["450nm", "415nm", "570nm", "675nm", "730nm", "850nm"]:
            if wavelength in path:
                images_dict[wavelength].append((img, path))
                break

    print("Paramètres de distorsion")
    dist_mtx_dict = {bande: get_file_matrice(bande) for bande in images_dict.keys()}

    print("Création d'une matrice optimale pour chaque bande")
    for bande in images_dict.keys():
        dist, mtx = dist_mtx_dict[bande]
        h, w = images_dict[bande][0][0].shape[:2]
        new_camera_mtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        print(f"Calcul de la correction pour {bande}")
        undistort_bande(images_dict[bande], mtx, dist, roi, new_camera_mtx)

if __name__ == "__main__":
    main("C:/Users/AHUMEAU/Desktop/transfert/Stage/2024 - Copie/*")