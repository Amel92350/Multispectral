import unittest
from main import indice
import cv2,os
import numpy as np

class TestIndice(unittest.TestCase):

    def setUp(self):
        #Setup initial conditions if needed
        self.panoramaA = np.zeros((100,100,3),dtype = np.uint8)
        self.panoramaB = np.ones((100,100,3),dtype = np.uint8)*128

    def test_calcul(self):
        result = indice.calcul(self.panoramaA,self.panoramaB)
        self.assertEqual(result.shape,self.panoramaA.shape)

    def test_testErreur(self):
        with self.assertRaises(FileNotFoundError):
            indice.testErreur(None,self.panoramaB)

    def test_rv(self):
        result = indice.rv(self.panoramaA,self.panoramaB)
        self.assertEqual(result.shape,self.panoramaA.shape)

    def test_sal(self):
        result = indice.sal(self.panoramaA, self.panoramaB)
        self.assertEqual(result.shape, self.panoramaA.shape)
       
    def test_org(self):
        result = indice.org(self.panoramaA, self.panoramaB)
        self.assertEqual(result.shape, self.panoramaA.shape)
     

    def test_SAVI(self):
        result = indice.SAVI(self.panoramaA, self.panoramaB)
        self.assertEqual(result.shape, self.panoramaA.shape)
        
class TestMainFunction(unittest.TestCase):

    def test_main_rv(self):
        # Test main function with Ic = "text"
        panoramas_path = "C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe5/panoramas"
        indice.main(panoramas_path, Ic="text")
        self.assertTrue(os.path.exists(os.path.join(panoramas_path, "rv.tif")))

    def test_main_sal(self):
        # Test main function with Ic = "sal"
        panoramas_path = "C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe5/panoramas"
        indice.main(panoramas_path, Ic="sal")
        self.assertTrue(os.path.exists(os.path.join(panoramas_path, "sal.tif")))

    def test_main_org(self):
        # Test main function with Ic = "org"
        panoramas_path = "C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe5/panoramas"
        indice.main(panoramas_path, Ic="org")
        
        self.assertTrue(os.path.exists(os.path.join(panoramas_path, "org.tif")))

    def test_main_savi(self):
        # Test main function with Ic = "savi"
        panoramas_path = "C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe5/panoramas"
        indice.main(panoramas_path, Ic="savi")
        # Assert that savi.tif was created
        self.assertTrue(os.path.exists(os.path.join(panoramas_path, "savi.tif")))
    
if __name__ == "__main__":
    unittest.main()