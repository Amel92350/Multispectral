import unittest
import cv2
import numpy as np
import os
from main import rescale

class TestRescale(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_images'
        os.makedirs(self.test_dir, exist_ok = True)

        self.image_paths = []
        for i in range(5):
            img = np.ones((100,100,3),dtype = np.uint8)* (i*50)
            path = os.path.join(self.test_dir,f'test_images_{i}.tif')
            cv2.imwrite(path,img)
            self.image_paths.append(path)

    def tearDown(self):
        for path in self.image_paths:
            os.remove(path)
        os.rmdir(self.test_dir)

    def test_Openimage(self):
        img,long,haut,  = rescale.Openimage(self.image_paths[0],[],[])
        self.assertIsNotNone(img)
        self.assertEqual(len(long),1)
        self.assertEqual(len(haut),1)
        self.assertEqual(long[0],100)
        self.assertEqual(haut[0],100)

    def test_recadrage(self):
        images = [cv2.imread(path,cv2.IMREAD_GRAYSCALE) for path in self.image_paths]
        l, r, t, b = rescale.recadrage(images)
        self.assertGreaterEqual(l,0)
        self.assertGreaterEqual(r,0)
        self.assertGreaterEqual(t,0)
        self.assertGreaterEqual(b,0)

    def test_resize_images_to_common_dimensions(self):
        rescale.resize_images_to_common_dimensions(self.image_paths)
        for path in self.image_paths:
            img = cv2.imread(path)
            self.assertEqual(img.shape[0],100)
            self.assertEqual(img.shape[1],100)

    def test_align_img(self):
        rescale.align_img(self.image_paths)
        for path in self.image_paths:
            img  = cv2.imread(path)
            self.assertIsNotNone(img)

    def test_mediane(self):
        kernel_size = 3
        rescale.mediane(self.image_paths,kernel_size)
        for path in self.image_paths:
            img = cv2.imread(path)
            self.assertIsNotNone(img)
    
if __name__ == "__main__":
    unittest.main()