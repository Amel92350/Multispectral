from main import image_raster_calculator as ir
import unittest
import numpy as np
import os, cv2
from unittest.mock import patch, mock_open, MagicMock

class TestImageRasterCalculator(unittest.TestCase):

    @patch('os.listdir')
    def test_get_image_files(self,mock_listdir):
        mock_listdir.return_value = ['image1.tif','image2.tif','not_image.txt']
        calculator = ir.ImageRasterCalculator('test_folder')
        expected_files = ["test_folder\\image1.tif","test_folder\\image2.tif"]
        self.assertEqual(calculator.image_files,expected_files)

    @patch('cv2.imread')
    @patch('os.listdir')
    def test_load_images(self,mock_listdir,mock_imread):
        mock_imread.side_effect=lambda x,flag: np.zeros((100,100),dtype = np.uint8) if 'image' in x else None
        calculator = ir.ImageRasterCalculator('test_folder')
        calculator.image_files = ['test_folder\\image1.tif','test_folder\\image2.tif']
        images = calculator.load_images()
        self.assertEqual(len(images),2)
        self.assertIn('image1',images)
        self.assertIn('image2',images)
        self.assertEqual(images['image1'].shape,(100,100))

    @patch('builtins.open',new_callable=mock_open,read_data="415nm + 450nm")
    @patch('os.listdir')
    def test_read_expression(self,mock_listdir,mock_file):
        calculator = ir.ImageRasterCalculator('test_folder')
        expression = calculator.read_expression('dummy_path')
        self.assertEqual(expression,'415nm + 450nm')
    @patch('os.listdir')
    def test_normalize_image(self,mock_listdir):
        calculator = ir.ImageRasterCalculator('test_folder')
        image = np.array([[0,128,255]],dtype = np.uint8)
        normalized_image = calculator.normalize_image(image)
        expected_image = np.array([[0,128,255]],dtype = np.uint8)
        np.testing.assert_array_equal(normalized_image,expected_image)


    @patch('cv2.add')
    @patch('cv2.subtract')
    @patch('cv2.multiply')
    @patch('cv2.divide')
    @patch('os.listdir')
    def test_evaluate_expression(self, mock_listdir,mock_divide, mock_multiply, mock_subtract, mock_add):
        

        def debug_mock(mock_func, name):
            def wrapper(x, y):
                result = mock_func(x, y)
                print(f"{name}: {x} {name} {y} -> {result}")
                return result
            return wrapper

       # Configurer les effets de côté pour les fonctions cv2
        mock_add.side_effect = debug_mock(lambda x, y:x+y, 'add')
        mock_subtract.side_effect = debug_mock(lambda x,y:x-y, 'subtract')
        mock_multiply.side_effect = debug_mock(lambda x,y:x*y, 'multiply')
        mock_divide.side_effect = debug_mock(lambda x,y:x/y, 'divide')

        calculator = ir.ImageRasterCalculator('test_folder')
        calculator.images = {
            '415nm': np.uint8([[2]]),
            '450nm': np.uint8([[2]])
        }
        expression = "415nm / 450nm"
        print(expression)
        result = calculator.evalutate_expression(expression)

        print("Final Result:", result)

        np.testing.assert_array_equal(result, np.array([[1]], dtype=np.uint8))

    @patch('cv2.imwrite')
    @patch('os.listdir')
    def test_save_image(self,mock_listdir,mock_imwrite):
        mock_imwrite.return_value = True 
        calculator = ir.ImageRasterCalculator('test_folder')
        image = np.zeros((100,100),dtype = np.uint8)
        calculator.save_image(image,'output.tif')
        mock_imwrite.assert_called_once_with('output.tif',image)
    
    
    @patch('cv2.imwrite')
    @patch('os.listdir')
    def test_save_image_error(self, mock_listdir,mock_imwrite):
        mock_imwrite.return_value = False
        calculator = ir.ImageRasterCalculator('test_folder')
        image = np.zeros((100, 100), dtype=np.uint8)
        with self.assertRaises(IOError):
            calculator.save_image(image, 'output.tif')

if __name__ == "__main__":
    unittest.main()
