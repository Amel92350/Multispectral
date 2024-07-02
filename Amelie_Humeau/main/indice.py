import cv2
import glob
import os
# from main import histogramme as h
import histogramme as h
from PIL import Image
import numpy as np

def calcul(orthomosaicA,orthomosaicB,ajustement=0):
    subtracted = cv2.subtract(orthomosaicA,orthomosaicB)
    added = cv2.add(orthomosaicA,orthomosaicB,ajustement)

    divided = cv2.divide(subtracted,added,scale = 256)
    divided = cv2.multiply(divided,(1+ajustement))

    return divided


def testErreur(orthomosaicA,orthomosaicB):
    if orthomosaicA is None or orthomosaicB is None:
        raise FileNotFoundError("Les images nécessaires n'ont pas été trouvées dans le répertoire spécifié.")

    if orthomosaicA.shape != orthomosaicB.shape:
       orthomosaicA = cv2.resize(orthomosaicA, (orthomosaicB.shape[1], orthomosaicB.shape[0]))

    if orthomosaicA.shape != orthomosaicA.shape:
        raise ValueError("Les tailles des images ne correspondent pas.")


def rv(orthomosaic_r,orthomosaic_v):

    testErreur(orthomosaic_r,orthomosaic_v)
    divided = calcul(orthomosaic_r,orthomosaic_v)
    return divided

def sal(orthomosaic_swir,orthomosaic_v):
   
    testErreur(orthomosaic_swir,orthomosaic_v)
    divided = calcul(orthomosaic_swir,orthomosaic_v)
    return divided

def org(orthomosaic_r,orthomosaic_nir):
    
    testErreur(orthomosaic_r,orthomosaic_nir)
    divided = calcul(orthomosaic_r,orthomosaic_nir)
    return divided


def SAVI(orthomosaic_r,orthomosaic_nir):
   
    testErreur(orthomosaic_r,orthomosaic_nir)
    divided = calcul(orthomosaic_nir,orthomosaic_r,ajustement = 0.5)
    return divided


def main(orthomosaic_path,Ic="text"):
    
    orthomosaic_uv = None
    orthomosaic_b = None
    orthomosaic_v = None
    orthomosaic_r = None
    orthomosaic_nir = None
    orthomosaic_swir = None

    orthomosaics = glob.glob(os.path.join(orthomosaic_path,"*.tif"))

    for orthomosaic in orthomosaics:
        
        if "415nm" in orthomosaic:
            orthomosaic_uv =Image.open(orthomosaic)
            orthomosaic_uv = np.array(orthomosaic_uv)
        elif "450nm" in orthomosaic: 
            orthomosaic_b =Image.open(orthomosaic)
            orthomosaic_b = np.array(orthomosaic_b)
        elif "570nm" in orthomosaic:
            orthomosaic_v =Image.open(orthomosaic)
            orthomosaic_v = np.array(orthomosaic_v)
        elif "675nm" in orthomosaic:
            orthomosaic_r =Image.open(orthomosaic)
            orthomosaic_r = np.array(orthomosaic_r)
        elif "730nm" in orthomosaic:
            orthomosaic_nir =Image.open(orthomosaic)
            orthomosaic_nir = np.array(orthomosaic_nir)
        elif "850nm" in orthomosaic :
            orthomosaic_swir =Image.open(orthomosaic)
            orthomosaic_swir = np.array(orthomosaic_swir)


    if Ic == "text":
        divided = rv(orthomosaic_r,orthomosaic_v)
        divided = h.etirer_min_max(divided)
        cv2.imwrite(os.path.join(orthomosaic_path, "rv.tif"), divided)

    elif Ic == "sal":
        divided = sal(orthomosaic_swir,orthomosaic_v)
        divided = h.etirer_min_max(divided)
        cv2.imwrite(os.path.join(orthomosaic_path, "sal.tif"), divided)
    
    elif Ic == "org":
        divided = org(orthomosaic_r, orthomosaic_nir)
        divided = h.etirer_min_max(divided)
        cv2.imwrite(os.path.join(orthomosaic_path,"org.tif"),divided)
    
    elif Ic == "savi":
        divided = SAVI(orthomosaic_r,orthomosaic_nir)
        #divided = h.etirer_min_max(divided)
        cv2.imwrite(os.path.join(orthomosaic_path,"savi.tif"),divided)


if __name__ == "__main__":
    main("C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe5/panoramas",Ic = "savi")
