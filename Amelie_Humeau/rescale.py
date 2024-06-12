# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 09:33:57 2021

@author: PAORAIN
"""
import matplotlib.pyplot as plt
import glob
import os
from PIL import Image
import numpy as np
import cv2 as cv
import tkinter.filedialog as FD

def Openimage(path,long=[],haut=[]):
    
    tmp= cv.imread(path, cv.IMREAD_UNCHANGED)

    
    h, w = tmp.shape[:2]
    long.append(w)
    haut.append(h)
    
    
    return tmp,long,haut


def recadrage(T):

    left = [0]
    right = [0]
    top = [0]
    bottom = [0]

    for image in T :
            
        w,h = image.shape

        pixels_left = 0
        pixels_right = 0
        pixels_top = 0
        pixels_bottom = 0

        for i in range(w):
            if(image[i,h//2])==0:
                pixels_left += 1
                i += 1
            else:
                break
            
        for i in range(1,w):
            if(image[-i,h//2])==0:
                pixels_right += 1
                i += 1
            else:
                break

        for j in range(h):
            if(image[w//2,j])==0:
                pixels_top += 1
                j += 1
            else:
                break

        for j in range(1,h):
            if(image[w//2,-j])==0:
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

    return l,r,t,b

def resize_images_to_common_dimensions(images):

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
    I=[]
    T=[]
    print("Aligning images ... ")
    for path in images:
        print(path)
        img= cv.imread(path, cv.IMREAD_UNCHANGED)
        I.append(img)
    
    if(I):
        alignMTB = cv.createAlignMTB()
        alignMTB.process(I, I)
        cpt=0
    
        for image in I:
            img=cv.cvtColor(image, cv.COLOR_BGR2GRAY )
            cv.imwrite(images[cpt],img)
            T.append(img)
            cpt+=1

        

        i = 0
        l,r,t,b = recadrage(T)
        for image in T:
            w,h = image.shape
            res = image[l:w-r,t:h-b]
            cv.imwrite(images[i],res)
            i+=1

def mediane(images,kernel):
    
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

    