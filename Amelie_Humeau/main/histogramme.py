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
        if(tab[i]!=0)and tab[i]>=100:
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
    new_img = np.zeros_like(img)
    hist = calculer_histogramme(img)
    max_v = get_indice_max(hist)
    min_v = get_indice_min(hist)


    if max_v == 0:
        return img

    if max_v - min_v == 0:
        return np.ones_like(img) *255

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i,j] = 255*((img[i,j]-min_v)/max_v-min_v)
    return new_img

def main(input_img):
    """
    Teste etirer min max sur une image
    """
    img = np.ones((10,10),dtype = np.uint8)*127
    new_img = etirer_min_max(img)
    hist_img = calculer_histogramme(img)
    hist_new_img = calculer_histogramme(new_img)
    plt.plot(hist_img,'red')
    plt.plot(hist_new_img,'green')
    plt.show()
    

if __name__ == "__main__":
    main("C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe5/panoramas/savi.tif")
