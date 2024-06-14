# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 10:30:58 2021

@author: PAORAIN
"""
import glob
import os

##### main #####
def main(src_path,dest_path):
    """
    Entrez le chemin absolue du dossier dans lequel 
    se trouve les images, suivie de /*/*.tif
    """
   
    
    images = glob.glob(src_path + "/*/*.tif")
    #tri des images
    for path in images:
        
        print(path)
        l = len(path)
        fim=path[l-25:l-10]
        
        if path.endswith("415nm.tif"):
            if not os.path.exists(dest_path+ "/415nm/"):
                os.makedirs(dest_path+ "/415nm/")
        elif path.endswith("450nm.tif"):
            if not os.path.exists(dest_path+ "/450nm/"):
                os.makedirs(dest_path+ "/450nm/")
            
        elif path.endswith("570nm.tif"):
            if not os.path.exists(dest_path+ "/570nm/"):
                os.makedirs(dest_path+ "/570nm/")
        elif path.endswith("675nm.tif"):
            if not os.path.exists(dest_path+ "/675nm/"):
                os.makedirs(dest_path+ "/675nm/")
        elif path.endswith("730nm.tif"):
            if not os.path.exists(dest_path+ "/730nm/"):
                os.makedirs(dest_path+ "/730nm/")
        elif path.endswith("850nm.tif"):
            if not os.path.exists(dest_path+ "/850nm/"):
                os.makedirs(dest_path+ "/850nm/")
    
    
if __name__ == "__main__":
    main("C:/Users/AHUMEAU/Desktop/photos","C:/Users/AHUMEAU/Desktop/photos")