import numpy as np
import imutils
import cv2
import glob
import rescale
from PIL import Image

def align_images_function(image,template,maxFeatures=500,keepPercent=0.2,debug=False):
    print("aligning images")
    #Convertit les deux images en niveaux de gris
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    #Utilisation d'ORB pour détecter les poitns clés et extraire 
    # les caractéristiques invariantes locales (binaires)
    orb = cv2.ORB_create(maxFeatures)
    (kpsA,descA) = orb.detectAndCompute(imageGray,None)
    (kpsB,descB) = orb.detectAndCompute(templateGray,None)

    #Correspondance
    method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    matcher = cv2.DescriptorMatcher_create(method)
    matches = matcher.match(descA,descB,None)

    #tri les correspondances par leur distance
    #Plus elles sont petite plus les features sont similaires
    matches = sorted(matches,key=lambda x:x.distance)

    keep = int(len(matches)*keepPercent)
    matches = matches[:keep]

    if debug:
        matchedVis = cv2.drawMatches(image,kpsA,template,kpsB,matches,None)
        matchedVis = imutils.resize(matchedVis,width=1000)
        cv2.imshow("Matched Keypoints", matchedVis)
        cv2.waitKey(0)
    

    #on alloue de la mémoire pour les point clés (x,y)
    ptsA = np.zeros((len(matches),2),dtype = float)
    ptsB = np.zeros((len(matches),2),dtype = float)

    for (i, m) in enumerate(matches):
        ptsA[i] = kpsA[m.queryIdx].pt
        ptsB[i] = kpsB[m.trainIdx].pt
    
    (H,mask) = cv2.findHomography(ptsA,ptsB,method = cv2.RANSAC)

    (h,w) = template.shape[:2]
    aligned = cv2.warpPerspective(image,H,(w,h))
    
    return aligned

def is_equal_to(image1,image2):
    if image1.shape == image2.shape:
        return (image1==image2).all()
    else:
        return False


def align_folder(images):
    print("[INFO] loading images...")

    T = []
    template = np.array(Image.open((images[0])))
    template = imutils.resize(template, width=700)
    for path in images:

        image = np.array(Image.open((path)))
        if not is_equal_to(template,image):
            
            aligned = align_images_function(image,template)

            print("[INFO] aligning images...")

            aligned = imutils.resize(aligned, width=700)
            
            
            stacked = np.hstack([aligned, template])


            aligned_gray = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY)
            

            T.append(aligned_gray)
            # cv2.imwrite(path,aligned)
            cv2.imshow("Image Alignement Stacked", stacked)
            cv2.waitKey(0)
        else:
            print(f"images égales {path} {images[0]}")

        print(len(T))
        l, r, t, b = rescale.recadrage(T)
        for i, image in enumerate(T):
            if image is None or image.size == 0:
                print(f"Error: Image for cropping at index {i} is empty.")
                continue
            h, w = image.shape
            res = image[l:h - r, t:w - b]
            if res is None or res.size == 0:
                print(f"Error: Cropped image at index {i} is empty.")
                continue
            cv2.imwrite(images[i], res)

def main(folders_dir,onedir = False): 

    """
    Folder_dir est le dossier contenant les prises de vue
    si onedir = True c'est une prise de vue
    """

    if onedir:
        images = glob.glob(folders_dir+"/*.tif")
        align_folder(images)

    folders = glob.glob(folders_dir)
    
    for folder in folders:
        images = glob.glob(folder+"/*.tif")
        if images:
            align_folder(images)

if __name__ == "__main__":
    main("C:\\Users\\AHUMEAU\\Desktop\\transfert\Stage\\2024 - Copie\\copied_images\\20210814_092734",onedir = True)