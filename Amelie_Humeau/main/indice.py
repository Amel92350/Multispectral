import cv2
import glob
import os
# from main import histogramme as h
import histogramme as h
from PIL import Image
import numpy as np

def calcul(panoramaA,panoramaB,ajustement=0):
    subtracted = cv2.subtract(panoramaA,panoramaB)
    added = cv2.add(panoramaA,panoramaB,ajustement)

    divided = cv2.divide(subtracted,added,scale = 256)
    divided = cv2.multiply(divided,(1+ajustement))

    return divided


def testErreur(panoramaA,panoramaB):
    if panoramaA is None or panoramaB is None:
        raise FileNotFoundError("Les images nécessaires n'ont pas été trouvées dans le répertoire spécifié.")

    if panoramaA.shape != panoramaB.shape:
        panoramaA = cv2.resize(panoramaA, (panoramaB.shape[1], panoramaB.shape[0]))

    if panoramaA.shape != panoramaA.shape:
        raise ValueError("Les tailles des images ne correspondent pas.")


def rv(panorama_r,panorama_v):

    testErreur(panorama_r,panorama_v)
    divided = calcul(panorama_r,panorama_v)
    return divided

def sal(panorama_swir,panorama_v):
   
    testErreur(panorama_swir,panorama_v)
    divided = calcul(panorama_swir,panorama_v)
    return divided

def org(panorama_r,panorama_nir):
    
    testErreur(panorama_r,panorama_nir)
    divided = calcul(panorama_r,panorama_nir)
    return divided


def SAVI(panorama_r,panorama_nir):
   
    testErreur(panorama_r,panorama_nir)
    divided = calcul(panorama_nir,panorama_r,ajustement = 0.5)
    return divided


def main(panoramas_path,Ic="text"):
    
    panorama_uv = None
    panorama_b = None
    panorama_v = None
    panorama_r = None
    panorama_nir = None
    panorama_swir = None

    panoramas = glob.glob(os.path.join(panoramas_path,"*.tif"))

    for panorama in panoramas:
        
        if "415nm" in panorama:
            panorama_uv = cv2.imread(panorama)
        elif "450nm" in panorama: 
            panorama_b = cv2.imread(panorama)
        elif "570nm" in panorama:
            panorama_v =Image.open(panorama)
            panorama_v = np.array(panorama_swir)
        elif "675nm" in panorama:
            panorama_r =Image.open(panorama)
            panorama_r = np.array(panorama_swir)
        elif "730nm" in panorama:
            panorama_nir =Image.open(panorama)
            panorama_nir = np.array(panorama_swir)
        elif "850nm" in panorama :
            panorama_swir =Image.open(panorama)
            panorama_swir = np.array(panorama_swir)


    if Ic == "text":
        divided = rv(panorama_r,panorama_v)
        divided = h.etirer_min_max(divided)
        cv2.imwrite(os.path.join(panoramas_path, "rv.tif"), divided)

    elif Ic == "sal":
        divided = sal(panorama_swir,panorama_v)
        divided = h.etirer_min_max(divided)
        cv2.imwrite(os.path.join(panoramas_path, "sal.tif"), divided)
    
    elif Ic == "org":
        divided = org(panorama_r, panorama_nir)
        divided = h.etirer_min_max(divided)
        cv2.imwrite(os.path.join(panoramas_path,"org.tif"),divided)
    
    elif Ic == "savi":
        divided = SAVI(panorama_r,panorama_nir)
        #divided = h.etirer_min_max(divided)
        cv2.imwrite(os.path.join(panoramas_path,"savi.tif"),divided)


if __name__ == "__main__":
    main("C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe5/panoramas",Ic = "savi")
