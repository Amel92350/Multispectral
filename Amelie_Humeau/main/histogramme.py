import numpy as np
import matplotlib.pyplot as plt
import glob, os, cv2

def calculer_histogramme(img):
    """
    Calcule l'histogramme de l'image donnée.
    :param img: Image en entrée
    :return: Histogramme de l'image
    """
    h = np.zeros((256))
    for p in img.ravel():
        h[p] += 1
    
    return h

def get_indice_max(tab):
    """
    Retourne l'indice de la valeur la plus haute d'un histogramme
    :param tab: Tableau 1 dimension en entrée
    :return: indice max
    """
    i_max =0

    for i in range(0,len(tab)-1):
        if tab[i]>0:
            i_max = i

    return i_max

def get_indice_min(tab):

    i_min = tab[-1]
    for i in range(len(tab)-1):
        if(tab[i]!=0):
            i_min = i
            break
    return i_min

def etirer_min_max(img):
    """
    Retourne la nouvelle image étirer aux min et max
    :param img: Image en entrée
    :return: indice max
    """
    
    hist = calculer_histogramme(img)
    
    max_v = get_indice_max(hist)
    min_v = get_indice_min(hist)
    
    if max_v == 0:
        return img

    if max_v - min_v == 0:
        return np.ones_like(img) *255

    normalized_img = 255 * ((img - min_v)/(max_v-min_v))
    normalized_img = np.clip(normalized_img, 0, 255).astype(int)


    new_img = np.clip(new_img,0,255).astype(np.uint8)

    return new_img



def main(input_folder):

    image_paths = glob.glob(input_folder + "/*.tif")
    for path in image_paths:
        print(path)
        if os.path.isfile(path):
            image = cv2.imread(path)
            etiree = etirer_min_max(image)
            cv2.imwrite(path,etiree)

def test(input_img):
    """
    Teste etirer min max sur une image
    """
    img = cv2.imread(input_img)
    new_img = etirer_min_max(img)
    cv2.imshow("image" , img)
    cv2.waitKey(0)
    cv2.imshow("image etiree",new_img)
    cv2.waitKey(0)
    

if __name__ == "__main__":
    test("C:/Users/AHUMEAU/Desktop/donnees_triees_test/570nm/20210814_093834570nm.tif")
