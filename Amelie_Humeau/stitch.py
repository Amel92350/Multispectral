import cv2
import glob
import time
import numpy as np
import matplotlib.pyplot as plt
import os
import imutils

cv2.ocl.setUseOpenCL(False)

def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    print(image.shape[2])
    return np.resize(image,(width, height))


def stitch_images(images):
    stitcher = cv2.Stitcher_create()
    status, result = stitcher.stitch(images)
    return status, result


def check_bande(chemin):
    if "415nm" in chemin: 
        return "415nm"
    elif "450nm" in chemin :
        return "450nm"
    elif "570nm" in chemin :
        return "570nm"
    elif "675nm" in chemin :
        return "675nm"
    elif "730nm" in chemin :
        return "730nm"
    else : 
        return "850nm" 
    
def EraseFolder(repertoire):
    import os

    files=os.listdir(repertoire)
    for i in range(0,len(files)):
        os.remove(repertoire+'/'+files[i])

    #ligne additionnelle si on veut suppimer le repertoire
    os.removedirs(repertoire)

def main(path_folder):

    if os.path.exists(path_folder + "/panoramas"):
        EraseFolder(path_folder + "/panoramas")
    

    folders = glob.glob(path_folder + "/*")

    for folder in folders:
        images = glob.glob(folder + "/*.tif")
        bande = check_bande(images[0])
        print(bande)
        image_bande = [cv2.imread(path).astype(np.uint8) for path in images]
        status = 1  
        status, result = stitch_images(image_bande)

        if status == cv2.STITCHER_OK:
            print(f"Panorama de la bande {bande} généré avec succès")
        
            if not os.path.exists(path_folder + "/panoramas"):
                os.makedirs(path_folder + "/panoramas")
            
            cv2.imwrite(path_folder + "/panoramas/" + bande + ".tif", result)
            # plt.imshow(result,cmap="gray")
            # plt.show()

            
        else:
            print(f"Échec de la génération du panorama code erreur : {status}")
   
        


if __name__ == "__main__":
    main("C:/Users/AHUMEAU/Desktop/donnees_triees")