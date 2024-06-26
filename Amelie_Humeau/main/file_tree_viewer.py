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

        # Ajouter un bouton pour ouvrir un dossier
        self.open_button = ttk.Button(self.tree_frame, text="Open Folder", command=self.open_folder)
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
            # Load original image
            original_image = Image.open(path)

            # Resize original image if it exceeds frame dimensions
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()

            if original_image.width > frame_width or original_image.height > frame_height:
                original_image.thumbnail((frame_width, frame_height))

            self.original_image = original_image  # Save original image for zooming
            self.current_image = original_image.copy()  # Save a copy for display
            self.zoom_factor = 1.0  # Reset zoom factor
            self.show_image(original_image)

        except Exception as e:
            self.canvas.create_text(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, text=str(e))

    def show_image(self, image):
        # Convert Image to PhotoImage and display on canvas
        photo = ImageTk.PhotoImage(image)
        self.canvas.image = photo  # Keep a reference to prevent garbage collection
        self.canvas.delete("all")
        self.image_id = self.canvas.create_image(0, 0, anchor='nw', image=photo)
        self.canvas.config(scrollregion=self.canvas.bbox(self.image_id))

    def zoom_image(self, event):
        # Calculate zoom factor based on mouse wheel or button clicks
        if event.num == 4 or event.delta > 0:  # Scroll up
            self.zoom_factor *= 1.1
        elif event.num == 5 or event.delta < 0:  # Scroll down
            self.zoom_factor /= 1.1

        # Limit zoom factor to a reasonable range
        self.zoom_factor = min(max(self.zoom_factor, 0.1), 10.0)

        # Get current mouse position relative to the canvas
        mouse_x = self.canvas.canvasx(event.x)
        mouse_y = self.canvas.canvasy(event.y)

        # Calculate the new width and height based on zoom factor
        new_width = int(self.original_image.width * self.zoom_factor)
        new_height = int(self.original_image.height * self.zoom_factor)

        # Resize the image
        resized_image = self.original_image.resize((new_width, new_height))

        # Display the resized image
        self.show_image(resized_image)

        # Adjust the canvas view to center around the mouse position
        self.canvas.xview_moveto(mouse_x / new_width)
        self.canvas.yview_moveto(mouse_y / new_height)

    def reset_zoom(self, event):
        # Reset zoom factor to 1.0 (original size)
        self.zoom_factor = 1.0
        # Redisplay the original image
        self.show_image(self.original_image)


    def update_base_path(self,base_path):
        self.base_path=base_path
        self.tree.delete(*self.tree.get_children())
        if os.path.isdir(base_path):
            self.populate_tree(base_path)

if __name__ == "__main__":
    root = Tk()
    app = FileTreeApp(root)
    root.mainloop()
