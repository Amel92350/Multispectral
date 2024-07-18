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
    qui représente l'image.
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
    if minim == maxi:
        return img

    data_conv = np.array(np.rint((img - minim) / float(maxi - minim) * 255.0), dtype=np.uint8)
    return data_conv

def get_file_matrice(bande):
    """
    Fonction qui crée une matrice de coefficients de distorsion et une matrice de paramètres intrinsèques.
    ENTREE : une chaîne de caractères (bande) qui contient la bande dont on veut les matrices (ex : '450nm')
    SORTIE : deux matrices dans un tuple (dist, mtx)
    """
    #Initialisation des matrices à 0
    dist = np.zeros((1, 5))
    mtx = np.zeros((3, 3))
    
    current_dir = os.path.dirname(os.path.abspath(__file__))

    dist_txt_path = os.path.join(current_dir,'resources','dist_v2.txt')
    mtx_txt_path = os.path.join(current_dir,'resources','mtx.txt')


    with open(dist_txt_path) as f_dist, open(mtx_txt_path) as f_mtx:
        data_dist = f_dist.readlines()
        data_mtx = f_mtx.readlines()

        #Récupère les données dans data_dist pour les mettre dans dist
        for i, line_name in enumerate(data_dist):
            if line_name.strip() == bande:
                for line in data_dist[i + 1:i + 6]:
                    indice1, indice2, value = line.strip().split(' ')
                    dist[int(indice1), int(indice2)] = float(value)
                    
        #Récupère les données dans data_mtx pour les mettre dans mtx
        for i, line_name in enumerate(data_mtx):
            if line_name.strip() == bande:
                for line in data_mtx[i + 1:i + 6]:
                    indice1, indice2, value = line.strip().split(' ')
                    mtx[int(indice1), int(indice2)] = float(value)

    return dist, mtx

def undistort_bande(img_bande, mtx, dist, roi, new_camera_mtx):
    """
    Fonction qui applique la correction de distorsion sur une bande d'images.
    :param img_bande: Liste des tuples (image, chemin) pour une bande spécifique
    :param mtx: Matrice des paramètres intrinsèques
    :param dist: Matrice des coefficients de distorsion
    :param roi: Région d'intérêt de la nouvelle caméra
    :param new_camera_mtx: Nouvelle matrice de la caméra après correction
    """
    for img, path in img_bande:
        #corrige la distorsion en fonction des nouveaux paramètres de calibration
        dst = cv.undistort(img, mtx, dist, None, new_camera_mtx)
        dst = convert12to8(dst)
        x, y, w, h = roi
        #rogne l'image pour retirer les bords noirs de la correction
        dst = dst[y:y + h, x:x + w]
        cv.imwrite(path, dst)


def main(chemin):
    """
    Fonction principale qui gère le processus de correction des images.
    :param chemin: Chemin absolu du dossier contenant les images, suivi de /*
    """
    print(chemin)
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
    help(undistort_bande)
