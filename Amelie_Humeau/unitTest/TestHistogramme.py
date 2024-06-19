import unittest
import cv2
import numpy as np

from main import histogramme

class TestHistogramme(unittest.TestCase):

    def setUp(self):
        #Création d'images de test
        self.black_image = np.zeros((10,10), dtype = np.uint8)
        self.white_image = np.ones((10,10), dtype = np.uint8)*255
        self.gray_image = np.ones((10,10), dtype=np.uint8)*127
    
    def test_calculer_histogramme_black_img(self):
        hist = histogramme.calculer_histogramme(self.black_image)
        expected_hist = np.zeros(256)
        expected_hist[0] = 100 #10x10 pixels qui ont la valeur 0
        np.testing.assert_array_equal(hist,expected_hist)
    
    def test_calculer_histogramme_white_img(self):
        hist = histogramme.calculer_histogramme(self.white_image)
        expected_hist = np.zeros(256)
        expected_hist[255] = 100 #10x10 pixels qui ont la valeur 255
        np.testing.assert_array_equal(hist,expected_hist)
    
    def test_get_indice_max(self):
        tab = np.zeros(256)
        tab[50] = 600 #l'index 50 a la valeur 600
        index_max = histogramme.get_indice_max(tab)
        self.assertEqual(index_max,50)

    def test_etirer_min_max_black_image(self):
        new_img = histogramme.etirer_min_max(self.black_image)
        expected_img = np.zeros((10,10),dtype = np.uint8) #Devrait rester noir
        np.testing.assert_array_equal(new_img,expected_img)
    
    def test_etirer_min_max_white_image(self):
        new_img = histogramme.etirer_min_max(self.white_image)
        expected_img = np.ones((10,10),dtype=np.uint8)*255 #Devrait rester blanc
        np.testing.assert_array_equal(new_img,expected_img)

    def test_etirer_min_max_gray_image(self):
        new_img = histogramme.etirer_min_max(self.gray_image)
        #Devrait rendre l'image grise blanche comme ce sont toutes les même valeurs
        expected_img = np.ones((10,10),dtype = np.uint8)*255
        np.testing.assert_array_equal(new_img,expected_img)

if __name__ == "__main__":
    unittest.main()

