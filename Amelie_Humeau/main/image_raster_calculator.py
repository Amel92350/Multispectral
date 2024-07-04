import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImageRasterCalculator:
    def __init__(self, images_folder):
        self.images_folder = images_folder
        self.image_files = self.get_image_files(images_folder)
        self.images = self.load_images()

    def get_image_files(self, folder_path):
        """
        Renvoie la liste des chemins des fichiers d'images TIFF dans le dossier spécifié.
        """
        return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.tif')]

    def load_images(self):
        """
        Charge les images en tant que dictionnaire avec le nom de l'image (sans extension) comme clé.
        """
        images = {}
        for file in self.image_files:
            name = os.path.splitext(os.path.basename(file))[0]
            images[name] = cv2.imread(file, cv2.IMREAD_UNCHANGED)
        return images

    def read_expression(self, file_path):
        """
        Lit l'expression à partir d'un fichier texte.
        """
        with open(file_path, 'r') as file:
            expression = file.read().strip()
        return expression
    
    def normalize_image(self, image):
        """
        Normalise l'image pour s'assurer que toutes les valeurs de pixel sont dans la plage 0-255.
        """
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        return np.uint8(image)
    
    def debug(self, left, right, result):
        """
        Displays images for debugging purposes.
        """
        import matplotlib.pyplot as plt
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        ax1.imshow(left, cmap="gray")
        ax1.set_title('Left Image')
        ax2.imshow(right, cmap="gray")
        ax2.set_title('Right Image')
        ax3.imshow(result, cmap="gray")
        ax3.set_title('Result Image')
        plt.show()

    def evalutate_expression(self, expression, ajustement=0):
        """
        Évalue l'expression donnée sur les images disponibles dans le dossier.
        """
        constantes = ["415nm", "450nm", "570nm", "675nm", "730nm", "850nm"]

        def eval_expr(expr):
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


                    print(f"Before operation {op}: left={left}, right={right}")
                    
                    if op == '+':
                        left = np.uint8([[2]])
                        right = np.uint8([[1]])

                        # Conversion temporaire en np.int32 pour éviter le "capping"
                        result = cv2.add(np.int32(left), np.int32(right))

                        # Reconversion en np.uint8 si nécessaire
                        result = np.uint8(result)

                        print("Left:", left)
                        print("Right:", right)
                        print("Result:", result)

                    elif op == '-':
                        result = cv2.subtract(left, right)
                        print(left,right,result)
                        print("subtract")
                    elif op == '*':
                        result = cv2.multiply(left, right)
                        self.debug(left, right, result)
                        print("multiply")
                    elif op == '/':
                        right[right == 0] = 1  # Avoid division by zero
                        result = cv2.divide(left, right)
                        self.debug(left, right, result)
                        print("divide")

                    # Debug print of result
                    print(f"Result image ({op}):")
                    print(result)

                    return result
                
                
            # Gère les constantes (images)
            for const in constantes:
                if const in expr:
                    if const in self.images:
                        return self.images[const]
                    else:
                        raise ValueError(f"Image {const} introuvable.")

            # Gère les résultats temporaires stockés dans globals()
            if expr.startswith('#'):
                img_id = int(expr[1:])
                return globals().get(f'img_{img_id}', None)

            raise ValueError(f"Opérateur non supporté ou image introuvable dans l'expression : {expr}")

        # Traite l'ajustement dans l'expression
        if 'ajustement' in expression:
            expression = expression.replace('ajustement', str(ajustement))

        return eval_expr(expression)

    def save_image(self, image, output_path):
        """
        Enregistre l'image résultante à l'emplacement spécifié.
        """
        extension = os.path.splitext(output_path)[1].lower()
        if extension not in ['.tif', '.tiff', '.png', '.jpg', '.jpeg']:
            raise ValueError("Extension de fichier non supportée pour l'enregistrement.")
        
        success = cv2.imwrite(output_path, image)
        if not success:
            raise IOError(f"Erreur lors de l'enregistrement de l'image à {output_path}")

# Exemple d'utilisation
if __name__ == "__main__":
    left = np.uint8([[2]])
    right = np.uint8([[1]])

    calculator = ImageRasterCalculator("C:/Users/AHUMEAU/Desktop/Pontcharaud/donnees_triees_groupe4/orthos")
    calculator.images = {
        '415nm': np.uint8([[2]]),
        '450nm': np.uint8([[1]]) 
    }

    expression =  '415nm - 450nm'

    result = calculator.evalutate_expression(expression)