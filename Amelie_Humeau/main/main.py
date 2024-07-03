import tkinter as tk
from tkinter import ttk, messagebox
from file_entry import FileEntry 
from image_processor import ImageProcessor
from file_tree_viewer import FileTreeApp
from add_index_window import AddIndexWindow
from ttkthemes import ThemedTk
from image_raster_calculator import ImageRasterCalculator
import glob, cv2

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Logiciel de traitement d'images multispectrales")
        self.root.geometry("1000x700")
    
        self.root.set_theme("clearlooks")
        self.bg_color = self.root.tk.eval("ttk::style lookup TFrame -background")

        self.init_styles()
        self.init_menu()
        self.init_widgets()
        self.processor = ImageProcessor(
            self.src_pathentry, self.dest_pathentry, self.orthomosaic_pathentry,
            self.status_label, self.progress_bar, self.flou_var, self.blur_value, self.file_tree_app
        )

    def init_styles(self):
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TEntry', font=('Helvetica', 10))
        style.configure('TCheckbutton', font=('Helvetica', 10))
        style.configure('TLabelFrame', font=('Helvetica', 12, 'bold'), background=self.bg_color)
        style.configure('TFrame', background=self.bg_color)

    def init_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Quitter", command=self.quit_app)

        action_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Actions", menu=action_menu)
        action_menu.add_command(label="Lancer le traitement complet", command=lambda: self.processor.start_processing("full"))
        action_menu.add_command(label="Créer des orthomosaïques", command=lambda: self.processor.start_processing("panoramas"))

        indice_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Raster", menu=indice_menu)
        indice_menu.add_command(label="Ajouter un Raster", command=lambda: self.open_add_index_window("add"))
        indice_menu.add_command(label="Applique Raster", command=lambda: self.open_add_index_window("applique"))

    def init_widgets(self):
        labelframe = ttk.LabelFrame(self.root, text="Bienvenue", padding="10px")
        labelframe.pack(side=tk.TOP, expand=1, fill=tk.BOTH, padx=10, pady=10)

        self.src_pathentry = FileEntry(labelframe, label="Dossier source : ")
        self.dest_pathentry = FileEntry(labelframe, label="Dossier destination : ")
        self.orthomosaic_pathentry = FileEntry(labelframe, label="Dossier des orthomosaïques")

        self.src_pathentry.pack(expand=0, fill=tk.X, pady=5)
        self.dest_pathentry.pack(expand=0, fill=tk.X, pady=5)
        self.orthomosaic_pathentry.pack(expand=0, fill=tk.X, pady=5)

        status_frame = ttk.LabelFrame(labelframe, text="Statut", padding="10px")
        status_frame.pack(side=tk.BOTTOM, expand=1, fill=tk.X, padx=5, pady=5)

        self.status_label = ttk.Label(status_frame, text="Prêt")
        self.status_label.pack(side=tk.LEFT, expand=1, fill=tk.X)

        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress_bar.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=5)

        flou_frame = ttk.Frame(labelframe)
        flou_frame.pack(side=tk.TOP, expand=0, fill=tk.X, padx=5)

        self.flou_var = tk.BooleanVar()
        self.blur_value = tk.StringVar()

        def toggle_blur_entry():
            if self.flou_var.get():
                self.blur_entry.pack(side=tk.LEFT, expand=0, padx=5)
            else:
                self.blur_entry.pack_forget()

        self.blur_entry = ttk.Entry(flou_frame, textvariable=self.blur_value)
        flou_checkbox = ttk.Checkbutton(flou_frame, text="Appliquer une médiane", variable=self.flou_var, command=toggle_blur_entry)
        flou_checkbox.pack(expand=0, fill=tk.X)

        file_tree_frame = ttk.Frame(self.root)
        file_tree_frame.pack(side=tk.BOTTOM, expand=1, fill=tk.BOTH, padx=10, pady=10)
        self.file_tree_app = FileTreeApp(file_tree_frame)

        def update_file_tree_app(*args):
            dest_path = self.orthomosaic_pathentry.get_path()
            self.file_tree_app.update_base_path(dest_path)

        self.orthomosaic_pathentry.folder_path.trace_add("write", update_file_tree_app)
        ttk.Sizegrip(self.root).pack(side=tk.RIGHT, expand=0, fill=tk.Y, padx=5, pady=5)

    def quit_app(self):
        if not self.processor.is_processing():
            self.root.quit()
        else:
            messagebox.showinfo("Information", "Attendez que le traitement soit terminé avant de quitter.")

    def open_add_index_window(self, mode):
        def on_select(indices):
            orthos_path = self.orthomosaic_pathentry.get_path()
            orthos = glob.glob(orthos_path+"/*.tif")
            calculator = ImageRasterCalculator(orthos_path)
            for index in indices:
                with open(index,"r") as index_f:
                    expression = index_f.readlines()[0]
                if expression:
                    print(expression)
                    result = calculator.evalutate_expression(expression)
                    cv2.imwrite(orthos_path+"/test.tif",result)
        AddIndexWindow(self.root, on_select, mode)

def main():
    root = ThemedTk(theme="clearlooks")
    app = MainApplication(root)
    root.mainloop()

if __name__ == '__main__':
    main()
