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

def afficher_histogramme(hist):
    """
    Affiche l'histogramme donné.
    :param hist: Histogramme à afficher
    """
    plt.plot(hist)
    plt.show()

def densite(h):
    """
    Calcule la densité cumulative de l'histogramme.
    :param h: Histogramme en entrée
    :return: Densité cumulative normalisée
    """
    s = 0
    res = np.zeros_like(h)
    for i in range(len(h)):
        res[i] = s
        s += h[i]
    return res / s    

def egaliser(img):
    """
    Applique l'égalisation d'histogramme à l'image donnée.
    :param img: Image en entrée
    :return: Image égalisée
    """
    d_im = densite(calculer_histogramme(img))
    im_eq = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            im_eq[i, j] = np.round(d_im[img[i, j]] * 255)
    return im_eq
    
def decaler_histogramme(img, nb):
    """
    Décale l'histogramme de l'image de nb unités.
    :param img: Image en entrée
    :param nb: Nombre d'unités pour décaler l'histogramme
    :return: Image avec l'histogramme décalé
    """
    new_img = np.zeros_like(img)
    new_img = (img + nb) % 255
    
    return new_img

def get_indice_max(tab):
    i_max =-1

    for i in range(0,len(tab)-1):
        if(tab[i]!=0)and tab[i]>500:
            i_max = i

    return i_max
def etirer_min_max(img):
    new_img = np.zeros_like(img)
    hist = calculer_histogramme(img)
    max_v = get_indice_max(hist)
    min_v = 0
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i,j] = 255*((img[i,j]-min_v)/max_v-min_v)
    return new_img

def main(input_folder):
    
    images = glob.glob(input_folder + "/*.tif")
    for image in images:
        img = cv2.imread(image)
        img_etiree = etirer_min_max(img)
        cv2.imwrite(image,img_etiree)


def main_dec(input_folder, nb):
    """
    Décale l'histogramme de toutes les images du dossier donné.
    :param input_folder: Chemin du dossier contenant les images
    :param nb: Nombre d'unités pour décaler l'histogramme
    """
    image_paths = glob.glob(os.path.join(input_folder, "*/*.tif"))
    for path in image_paths:
        print(path)
        img = cv2.imread(path)
        img_dec = decaler_histogramme(img, nb)

        cv2.imwrite(path, img_dec)

def normalisation_images(input_folder):
    """
    Normalise toutes les images du dossier donné.
    :param input_folder: Chemin du dossier contenant les images
    """
    image_paths = glob.glob(os.path.join(input_folder, "*/*.tif"))
    for path in image_paths:
        img = cv2.imread(path)
        norm = (img - np.min(img)) / (np.max(img) - np.min(img))
        cv2.imwrite(path, norm)

def test_histogramme():
    """
    Teste l'égalisation d'histogramme sur une image spécifique.
    """
    print("test histogramme")
    img = plt.imread("C:/Users/AHUMEAU/Desktop/donnees_triees/850nm/20210814_092848_850nm.tif")
    print(img)

    img_eq = egaliser(img)

    fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout=False, figsize=(16, 9))
    ax1.imshow(img, cmap="gray")
    ax1.set_xlabel("Image", fontsize=14)
 
    ax2.imshow(img_eq, cmap="gray")
    ax2.set_xlabel("Image égalisée", fontsize=14)

    plt.show()    

if __name__ == "__main__":
    main("C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe5/panoramas")
