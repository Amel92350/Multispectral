import os
from tkinter import Tk, Frame, Label, filedialog
from tkinter import ttk
from PIL import Image, ImageTk

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

        # Arborescence
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill='both', expand=True)
        self.tree.bind("<Double-1>", self.on_tree_item_click)

        # Zone pour afficher l'image
        self.image_label = Label(self.image_frame, text="No image selected", anchor="center")
        self.image_label.pack(fill='both', expand=True)

        # Ajouter un bouton pour ouvrir un dossier
        self.open_button = ttk.Button(self.tree_frame, text="Open Folder", command=self.open_folder)
        self.open_button.pack(side='bottom', pady=10)

        self.base_path = ''  # Chemin pour le dossier ouvert
        self.original_image = None
        self.current_image = None
        self.zoom_factor = 1.0
        
        self.mouse_x = 0
        self.mouse_y = 0

        # Bind mouse wheel events for zooming
        self.image_label.bind("<MouseWheel>", self.zoom_image)
        self.image_label.bind("<Button-4>", self.zoom_image)
        self.image_label.bind("<Button-5>", self.zoom_image)
        self.image_label.bind("<Double-Button-1>",self.reset_zoom)

    def zoom_image(self,event):
        if event.num == 4 or event.delta > 0:  # Scroll up
            self.zoom_factor /= 1.1
        elif event.num == 5 or event.delta < 0:  # Scroll down
            self.zoom_factor *= 1.1

        self.zoom_factor = min(max(self.zoom_factor,0.1),1.0)

        self.mouse_x=event.x
        self.mouse_y = event.y

        self.show_zoommed_image(self.current_image)

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.base_path = folder_path  # Stocke le chemin de base
            self.tree.delete(*self.tree.get_children())
            self.populate_tree(folder_path)

    def populate_tree(self, folder_path, parent=''):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            item_id = self.tree.insert(parent, 'end', text=item, open=False)
            if os.path.isdir(item_path):
                self.populate_tree(item_path, item_id)

    def on_tree_item_click(self, event):
        selected_item = self.tree.selection()[0]
        item_path = self.get_full_path(selected_item)

        if os.path.isfile(item_path) and item_path.lower().endswith('.tif'):
            self.display_image(item_path)

    def get_full_path(self, item):
        parts = []
        while item:
            parts.insert(0, self.tree.item(item, 'text'))
            item = self.tree.parent(item)
        return os.path.join(self.base_path, *parts)

    def display_image(self, path):
        try:
            image = Image.open(path)
            self.original_image = image  # Save original image for zooming
            self.current_image = image.copy()  # Save a copy for modifications
            self.zoom_factor = 1.0  # Reset zoom factor
            self.show_image(image)
        except Exception as e:
            self.image_label.config(text=str(e))  # Debug: Afficher les erreurs d'ouverture d'image

    def show_image(self,image):

        image.thumbnail((self.image_frame.winfo_width(), self.image_frame.winfo_height()))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo, text='')
        self.image_label.image = photo

    def show_zoommed_image(self, image):
        # Resize image to fit in the frame while keeping aspect ratio

        zoomed_size = (
            int(image.width * self.zoom_factor),
            int(image.height * self.zoom_factor)
        )

        

        #Calculate coordinates to keep the mouse position fixed
        x0 = int(self.mouse_x - (self.mouse_x/zoomed_size[0])* self.image_frame.winfo_width())
        y0 = int(self.mouse_y - (self.mouse_y/zoomed_size[1])* self.image_frame.winfo_height())
        x1 = x0+self.image_frame.winfo_width()
        y1 = y0+self.image_frame.winfo_height()

        # Crop the image if it exceeds the frame size
        if x0 < 0:
            x0 = 0
        if y0 < 0:
            y0 = 0
        if x1 > image.width:
            x1 = image.width
        if y1 > image.height:
            y1 = image.height

        cropped_image = image.crop((x0,y0,x1,y1))

        resized_image = cropped_image.resize(zoomed_size)
        self.show_image(resized_image)

    def reset_zoom(self,event):
        self.zoom_factor = 1.0
        self.show_image(self.original_image)
    

    def update_base_path(self, base_path):
        self.base_path = base_path
        self.tree.delete(*self.tree.get_children())
        if os.path.isdir(base_path):
            self.populate_tree(base_path)

if __name__ == "__main__":
    root = Tk()
    app = FileTreeApp(root)
    root.mainloop()
