import cv2
import glob
import os
import numpy as np

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
    if os.path.exists(path_folder + "/panoramas"):
        EraseFolder(path_folder + "/panoramas")

    folders = glob.glob(path_folder + "/*")

    for folder in folders:
        images = glob.glob(folder + "/*.tif")
        bande = check_bande(images[0])

        image_bande = [cv2.imread(path).astype(np.uint8) for path in images]
        status = 1

        status, result = stitch_images(image_bande)

        if status == cv2.STITCHER_OK:
            print(f"Panorama de la bande {bande} généré avec succès")

            if not os.path.exists(path_folder + "/panoramas"):
                os.makedirs(path_folder + "/panoramas")

            cv2.imwrite(path_folder + "/panoramas/" + bande + ".tif", result)

        else:
            print(f"Échec de la génération du panorama code erreur : {status}")

if __name__ == "__main__":
    main("C:/Users/AHUMEAU/Desktop/donnees_triees_test")