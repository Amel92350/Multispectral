import os,cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols,sympify

class ImageRasterCalculator:
    def __init__(self,images_folder):
        self.images_folder = images_folder
        self.image_files = self.get_image_files(images_folder)
        self.images = self.load_images()


    def load_images(self):
        """
        Charge les images en tant que dictionnaire avec le nom de l'image (sans extension) comme clef
        """
        images = {}
        for file in self.image_files:
            name = os.path.splitext(os.path.basename(file))[0]
            images[name] = np.array(Image.open(file))

        return images

    def get_image_files(self,folder_path):
        """
        Renvoie la liste des chemins des fichiers d'images TIFF dans le dossier spécifique
        """
        image_files = [os.path.join(folder_path,f)for f in os.listdir(folder_path) if f.lower().endswith(".tif")]
        return image_files
    
    def read_expression(self,file_path):
        """
        Lit l'expression à partir d'un fichier texte.
        """
        with open(file_path,'r') as file:
            expression = file.readlines()[0]
            print(expression)
        return expression
    

    def evalutate_expression(self,expression):
        """
        Évalue l'expression donnée sur les images disponible dans le dossier
        """
        constantes = ["415nm","450nm","570nm","675nm","730nm","850nm"]
        
        def eval_expr(expression):
            expr =expression.replace(' ','')
            while "(" in expr and ")" in expr:
                start= expr.rfind("(")
                end = expr.find(')',start)
                sub_expr = expr[start+1:end]
                result = eval_expr(sub_expr)
                expr = expr[:start] + f'#{id(result)}' + expr[end+1:]
                globals()[f'img_{id(result)}'] = result

            for op in ["+","-","*","/"]:
                if op in expr:
                    parts = expr.split(op)
                    print(parts)
                    left = eval_expr(parts[0])
                    right = eval_expr(parts[1])

                    if left is None or right is None:
                        raise ValueError("Image non trouvée pour l'une des constantes dans l'expression.")

                    if op == '+':
                        return cv2.add(left,right)
                    elif op == '-':
                        return cv2.subtract(left,right)
                    elif op == '*':
                        return cv2.multiply(left,right)
                    elif op == '/':
                        right[right==0]=1
                        return cv2.divide(left,right)
                    
            for const in constantes:
                if const in expr:
                    return self.images[const]
                
            if expr.startswith('#'):
                img_id = int(expr[1:])
                return globals().get(f'img_{img_id}', None)
                
        return eval_expr(expression)                    


    def save_image(self, image, output_path):
        """
        Enregistre l'image résultante à l'emplacement spécifié.
        """
        extension = os.path.splitext(output_path)[1].lower()
        print(output_path,extension)
        if extension not in ['.tif', '.tiff', '.png', '.jpg', '.jpeg']:
            raise ValueError("Extension de fichier non supportée pour l'enregistrement.")
        
        success = cv2.imwrite(output_path, image)
        if not success:
            raise IOError(f"Erreur lors de l'enregistrement de l'image à {output_path}")
        
if __name__ == "__main__":
    images_folder = "C:/Users/AHUMEAU/Desktop/donnees_triees_test/panoramas"
    calculator = ImageRasterCalculator(images_folder)   
    expression_file ="C:/Users/AHUMEAU/git/Multispectral/Amelie_Humeau/main/calculs/indice_de_texture_des_sols.txt"
    expression = calculator.read_expression(expression_file) 
    try:
        result = calculator.evalutate_expression(expression)
        calculator.save_image(result,images_folder+'/test.tif')
        print(f"Resultat de l'expression '{expression}' : {result}")
        plt.imshow(result,cmap="gray")
        plt.show()
    except ValueError as e:
        print(f"Erreur: {str(e)}")

    