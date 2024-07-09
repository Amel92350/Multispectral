import cv2
import glob
import os
import numpy as np
import imutils

# Désactiver OpenCL pour éviter les problèmes potentiels
cv2.ocl.setUseOpenCL(False)

def resize_image(image, scale_percent):
    """
    Redimensionne une image.

    Parameters:
    image (numpy.ndarray): Image à redimensionner.
    scale_percent (int): Pourcentage d'échelle pour le redimensionnement.

    Returns:
    numpy.ndarray: Image redimensionnée.
    """
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    return np.resize(image, (width, height))

def stitch_images(images):
    """
    Assemble des images en un panorama.

    Parameters:
    images (list): Liste d'images à assembler.

    Returns:
    (int, numpy.ndarray): Statut de l'assemblage et panorama résultant.
    """
    stitcher = cv2.Stitcher_create()
    return stitcher.stitch(images)

def check_bande(chemin):
    """
    Détermine la bande en fonction du chemin de l'image.

    Parameters:
    chemin (str): Chemin de l'image.

    Returns:
    str: Bande de l'image.
    """
    if "415nm" in chemin:
        return "415nm"
    elif "450nm" in chemin:
        return "450nm"
    elif "570nm" in chemin:
        return "570nm"
    elif "675nm" in chemin:
        return "675nm"
    elif "730nm" in chemin:
        return "730nm"
    else:
        return "850nm"

def EraseFolder(repertoire):
    """
    Supprime tous les fichiers dans un répertoire.

    Parameters:
    repertoire (str): Répertoire à vider.
    """
    import os
    files = os.listdir(repertoire)
    for i in range(0, len(files)):
        os.remove(repertoire+'/'+files[i])

    os.removedirs(repertoire)

def main(path_folder):
    """
    Fonction principale pour assembler des images en panoramas par bande.

    Parameters:
    path_folder (str): Chemin du dossier contenant les images.
    """
    if os.path.exists(path_folder + "/orthos"):
        EraseFolder(path_folder + "/orthos")

    folders = glob.glob(path_folder + "/*")

    for folder in folders:
        images = glob.glob(folder + "/*.tif")
        bande = check_bande(images[0])

        image_bande = [cv2.imread(path).astype(np.uint8) for path in images]
        status = 1

        status, stitched = stitch_images(image_bande)

        if status == cv2.STITCHER_OK:
            print(f"Panorama de la bande {bande} généré avec succès")

            stitched = cv2.copyMakeBorder(stitched,10,10,10,10,cv2.BORDER_CONSTANT,(0,0,0))

            gray = cv2.cvtColor(stitched,cv2.COLOR_RGB2GRAY)
            thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)[1]

            cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts,key = cv2.contourArea)

            mask = np.zeros(thresh.shape,dtype = "uint8")
            (x,y,w,h) = cv2.boundingRect(c)
            cv2.rectangle(mask,(x,y),(x+w,y+h),255,-1)

            minRect = mask.copy()
            sub = mask.copy()

            while len(sub)-cv2.countNonZero(sub)>0:
                minRect = cv2.erode(minRect,None)
                sub = cv2.subtract(minRect,thresh)

            cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(c)
            
            result = stitched[y:y+h,x:x+w]


            if not os.path.exists(path_folder + "/orthos"):
                os.makedirs(path_folder + "/orthos")

            cv2.imwrite(path_folder + "/orthos/" + bande + ".tif", result)

        else:
            print(f"Échec de la génération du panorama code erreur : {status}")

if __name__ == "__main__":
    main("C:/Users/AHUMEAU/Desktop/test_5000")