from tkinter import Tk, Frame, Canvas, filedialog, ttk
from PIL import Image, ImageTk
import os

class FileTreeApp:
    def __init__(self, root, base_path=''):
        self.root = root

        self.style = ttk.Style()
        self.style.configure("Treeview", font=("Helvetica", 10))
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.style.configure("TLabel", font=("Helvetica", 12))

        # Frame pour l'arborescence à gauche
        self.tree_frame = Frame(root, bd=2, relief="sunken", padx=10, pady=10)
        self.tree_frame.pack(side='left', fill='both', expand=True)

        # Frame pour l'image à droite
        self.image_frame = Frame(root, bd=2, relief="sunken", padx=10, pady=10)
        self.image_frame.pack(side='right', fill='both', expand=True)

        # Canvas pour afficher l'image
        self.canvas = Canvas(self.image_frame)
        self.canvas.pack(fill='both', expand=True)

        # Bind mouse wheel events for zooming
        self.canvas.bind("<MouseWheel>", self.zoom_image)
        self.canvas.bind("<Button-4>", self.zoom_image)  # Scroll up
        self.canvas.bind("<Button-5>", self.zoom_image)  # Scroll down
        self.canvas.bind("<Double-Button-1>", self.reset_zoom)

        # Ajouter un bouton pour ouvrir l'explorateur de fichier
        self.open_button = ttk.Button(self.tree_frame, text="Ouvrir", command=self.open_folder)
        self.open_button.pack(side='bottom', pady=10)

        self.base_path = ''  # Chemin pour le dossier ouvert
        self.original_image = None
        self.current_image = None
        self.zoom_factor = 1.0
        self.image_id = None

        self.style = ttk.Style()
        self.style.configure("Treeview", font=("Helvetica", 10))
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.style.configure("TLabel", font=("Helvetica", 12))

        # Arborescence
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill='both', expand=True)
        self.tree.bind("<Double-1>", self.on_tree_item_click)

    def open_folder(self):
        """
        Ouvre une fenetre de dialiogue pour choisir un dossier pour peupler l'arbre
        """
        os.startfile(self.base_path)

    def populate_tree(self, folder_path, parent=''):
        """
        Peuple l'arbre récursivement avec le chemin de dossier donné 
        """
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            item_id = self.tree.insert(parent, 'end', text=item, open=False)
            if os.path.isdir(item_path):
                self.populate_tree(item_path, item_id)

    def on_tree_item_click(self,event):
        """
        Permet de gérer l'évenement quand on clique sur l'image, lance la méthode pour afficher l'image
        """
        selected_item = self.tree.selection()[0]
        item_path = self.get_full_path(selected_item)

        if os.path.isfile(item_path) and item_path.lower().endswith('.tif'):
            self.display_image(item_path)

    def get_full_path(self, item):
        """
        récupère le chemin complet de l'image
        """
        parts = []
        while item:
            parts.insert(0, self.tree.item(item, 'text'))
            item = self.tree.parent(item)
        return os.path.join(self.base_path, *parts)

    def display_image(self, path):
        """
        Affiche l'image
        """
        try:
            # Charge l'image originale
            original_image = Image.open(path)

            # Redimensionne l'image originale si sa taille excede la taille de la Frame
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()

            if original_image.width > frame_width or original_image.height > frame_height:
                original_image.thumbnail((frame_width, frame_height))

            self.original_image = original_image  # Sauvegarde l'image originale pour le zoom
            self.current_image = original_image.copy()  # Sauvegarde une copie pour l'affichage
            self.zoom_factor = 1.0  # Reset zoom factor
            self.show_image(original_image)

        except Exception as e:
            self.canvas.create_text(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, text=str(e))

    def show_image(self, image):
        # Convertit l'image en PhotoImage pour l'afficher dans le canvas
        photo = ImageTk.PhotoImage(image)
        self.canvas.image = photo  # Keep a reference to prevent garbage collection
        self.canvas.delete("all")
        self.image_id = self.canvas.create_image(0, 0, anchor='nw', image=photo)
        self.canvas.config(scrollregion=self.canvas.bbox(self.image_id))

    def zoom_image(self, event):
        """
        Permet de zoomer sur l'image avec la molette de la souris
        """
        # Calcul le facteur de zoom
        if event.num == 4 or event.delta > 0:  # Scroll up
            self.zoom_factor *= 1.1
        elif event.num == 5 or event.delta < 0:  # Scroll down
            self.zoom_factor /= 1.1

        # Limiter le facteur de zoom à une plage raisonnable
        self.zoom_factor = min(max(self.zoom_factor, 0.1), 10.0)

        # Récupérer la position actuelle de la souris sur le canvas
        mouse_x = self.canvas.canvasx(event.x)
        mouse_y = self.canvas.canvasy(event.y)

        # Calcule la nouvelle largeur et hauteur basées sur le facteur de zoom
        new_width = int(self.original_image.width * self.zoom_factor)
        new_height = int(self.original_image.height * self.zoom_factor)

        # Redimensionne l'image
        resized_image = self.original_image.resize((new_width, new_height))

        self.show_image(resized_image)

        # Ajuste la vue du canvas pour qu'elle soit centrée autour de la position de la souris.
        self.canvas.xview_moveto(mouse_x / new_width)
        self.canvas.yview_moveto(mouse_y / new_height)

    def reset_zoom(self,event):
        """
        Réinitialise la position de l'image
        """
        # Reset zoom factor to 1.0 (original size)
        self.zoom_factor = 1.0
        # Réaffiche l'image originale
        self.show_image(self.original_image)


    def update_base_path(self,base_path):
        """
        Met à jour le chemin de l'arbre et peple l'arbre avec ce chemin
        """
        #Enregistre le nouveau chemin de base
        self.base_path=base_path
        #Supprime l'ancienne arborescence
        self.tree.delete(*self.tree.get_children())
        #Peuple l'arbre avec le nouveau chemin
        if os.path.isdir(base_path):
            self.populate_tree(base_path)

if __name__ == "__main__":
    root = Tk()
    app = FileTreeApp(root)
    root.mainloop()
