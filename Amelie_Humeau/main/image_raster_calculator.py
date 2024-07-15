import os
import cv2
import numpy as np

class ImageRasterCalculator:

    def __init__(self, images_folder):
        self.images_folder = images_folder
        self.image_files = self.get_image_files(images_folder)
        self.images = self.load_images()

    def get_image_files(self, folder_path):
        """
        Renvoie la liste des chemins des fichiers d'images TIFF dans le dossier spécifié.
        """
        try:
            return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.tif')]
        except Exception as e:
            print(f"Erreur lors de la récupération des fichiers d'images TIFF dans le dossier : {folder_path}")
            return []
        
    def load_images(self):
        """
        Charge les images en tant que dictionnaire avec le nom de l'image (sans l'extension) comme clé.
        """
        images = {}
        for file in self.image_files:
            try :
                name = os.path.splitext(os.path.basename(file))[0]
                image = cv2.imread(file, cv2.IMREAD_UNCHANGED)
                if image is None:
                    print(f"Erreur lors du chargement de l'image : {file}")
                else:
                    images[name] = image
            except Exception as e:
                print(f"Erreur lors du chargement de l'image {file} : {str(e)}")

        return images

    def read_expression(self, file_path):
        """
        Lit l'expression à partir d'un fichier texte.
        """
        try:
            with open(file_path, 'r') as file:
                expression = file.read().strip()
            return expression
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier d'expression: {str(e)}")
            
    def normalize_image(self, image):
        """
        Normalise l'image pour s'assurer que toutes les valeurs de pixel sont dans la plage 0-255.
        """
        try:
            image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
            return np.uint8(image)
        except Exception as e:
            print(f"Erreur lors de la normalisation de l'image : {str(e)}")
            return image

    def evalutate_expression(self, expression):
        """
        Évalue l'expression donnée sur les images disponibles dans le dossier.
        """
        constantes = ["415nm", "450nm", "570nm", "675nm", "730nm", "850nm"]

        def eval_expr(expr):
            try:
                # Supprime les espaces
                expr = expr.replace(" ", "")

                # Gère les parenthèses
                while '(' in expr and ')' in expr:
                    start = expr.rfind('(')
                    end = expr.find(')', start)
                    sub_expr = expr[start + 1:end]
                    result = eval_expr(sub_expr)
                    expr = expr[:start] + f'#{id(result)}' + expr[end + 1:]
                    globals()[f'img_{id(result)}'] = result

                # Gère les opérations
                operators = ['+', '-', '*', '/']
                for op in operators:
                    if op in expr:
                        parts = expr.split(op)
                        left = eval_expr(parts[0])
                        right = eval_expr(parts[1])
                        
                        #Opération sur les parties :
                        
                        if op == '+':
                            result = cv2.add(left,right)
                            
                        elif op == '-':

                            result = cv2.subtract(left,right)
                        elif op == '*':

                            result = cv2.multiply(left,right)
                            
                        elif op == '/':

                            right[right == 0] = 1  # évite la division par zéro
                            result = cv2.divide(np.float32(left), np.float32(right))

                        return result
                    
                    
                # Gère les constantes (images)
                for const in constantes:
                    if const in expr:
                        if const in self.images:
                            return self.normalize_image(self.images[const])
                        else:
                            raise ValueError(f"Image {const} introuvable.")

                # Gère les résultats temporaires stockés dans globals()
                if expr.startswith('#'):
                    img_id = int(expr[1:])
                    return globals().get(f'img_{img_id}', None)

                raise ValueError(f"Opérateur non supporté ou image introuvable dans l'expression : {expr}")
            except Exception as e:
                print(f"Erreur lors de l'évaluation de l'expression '{expr}' ; {str(e)} ")
                return None
            
        return eval_expr(expression)

    def save_image(self, image, output_path):
        """
        Enregistre l'image résultante à l'emplacement spécifié.
        """
        try:
            extension = os.path.splitext(output_path)[1].lower()
            if extension not in ['.tif', '.tiff', '.png', '.jpg', '.jpeg']:
                raise ValueError("Extension de fichier non supportée pour l'enregistrement.")
            
            success = cv2.imwrite(output_path, image)
            if not success:
                raise IOError(f"Erreur lors de l'enregistrement de l'image à {output_path}")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de l'image : {str(e)}")

# Exemple d'utilisation
if __name__ == "__main__":
    calculator = ImageRasterCalculator("C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe4/orthos")
    
    

    expression =  '415nm + 450nm'

    result = calculator.evalutate_expression(expression)
    print(result)