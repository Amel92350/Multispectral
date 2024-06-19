import unittest
from main import Correction
import numpy as np
from unittest.mock import patch, mock_open
from PIL import Image
import os

class TestCorrection(unittest.TestCase):

    @patch('PIL.Image.open')
    def test_Openimage(self,mock_open):
        mock_img = np.zeros((10,10),dtype=np.uint8)
        mock_open.return_value = Image.fromarray(mock_img)
        img, path = Correction.Openimage("C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe5/450nm/20190529_095319450nm.tif")
        self.assertTrue(np.array_equal(img,mock_img))
        self.assertEqual(path,os.path.abspath("C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe5/450nm/20190529_095319450nm.tif"))

    def test_convert12to8(self):
        img = np.array([[0,4095],[2048,1024]])
        expected_img = np.array([[0,255],[128,64]])
        result_img = Correction.convert12to8(img)
        np.testing.assert_array_equal(result_img,expected_img)

    @patch("builtins.open",new_callable = mock_open,read_data ='450nm\n0 0 0.1\n0 1 0.2\n0 2 0.3\n0 3 0.4\n0 4 0.5\n415nm\n0 0 0.6\n0 1 0.7\n0 2 0.8\n0 3 0.9\n0 4 1.0\n')
    def test_get_file_matrice(self,mock_file):
        dist , mtx = Correction.get_file_matrice('450nm')
        expected_dist = np.array([[0.1,0.2,0.3,0.4,0.5]])
        expected_mtx = np.zeros((3,3))
        self.assertTrue(np.array_equal(dist,expected_dist))
        self.assertTrue(np.array_equal(mtx,expected_mtx))

    @patch("cv2.undistort")
    @patch("cv2.imwrite")
    def test_undistort_bande(self, mock_imwrite, mock_undistort):
        img = np.zeros((10, 10), dtype=np.uint8)
        path = "C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe5/450nm/20190529_095319450nm.tif"
        img_bande = [(img, path)]
        mtx = np.eye(3)
        dist = np.zeros((1, 5))
        roi = (0, 0, 10, 10)
        new_camera_mtx = np.eye(3)
        mock_undistort.return_value = img
        Correction.undistort_bande(img_bande, mtx, dist, roi, new_camera_mtx)
        mock_undistort.assert_called_once()
        args, kwargs = mock_imwrite.call_args
        self.assertEqual(args[0],path)
        np.testing.assert_array_equal(args[1],img)


    
if __name__ == "__main__":
    unittest.main()