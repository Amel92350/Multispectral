import tkinter as tk
from tkinter import ttk, messagebox
from file_entry import FileEntry
from image_processor import ImageProcessor
from file_tree_viewer import FileTreeApp
from add_index_window import AddIndexWindow

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Logiciel de traitement d'images multispectrales")
        self.root.geometry("1000x700")

        self.init_menu()
        self.init_widgets()
        self.processor = ImageProcessor(
            self.src_pathentry, self.dest_pathentry, self.orthomosaic_pathentry,
            self.status_label, self.progress_bar, self.flou_var, self.blur_value, self.file_tree_app
        )

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
        menu_bar.add_cascade(label="Indices", menu=indice_menu)
        indice_menu.add_command(label="Ajouter un indice", command=self.open_add_index_window)
        indice_menu.add_command(label="Indice de texture des sols", command=lambda: self.processor.process_index("text"))
        indice_menu.add_command(label="Indice de salinité", command=lambda: self.processor.process_index("sal"))
        indice_menu.add_command(label="Indice de matière organique", command=lambda: self.processor.process_index("org"))
        indice_menu.add_command(label="Indice de végétation ajusté pour le sol", command=lambda: self.processor.process_index("savi"))

    def init_widgets(self):
        labelframe = ttk.LabelFrame(self.root, text="Bienvenue", padding="5px")
        labelframe.pack(side=tk.TOP, expand=1, fill=tk.BOTH, padx=5, pady=5)

        self.src_pathentry = FileEntry(labelframe, label="Dossier source : ")
        self.dest_pathentry = FileEntry(labelframe, label="Dossier destination : ")
        self.orthomosaic_pathentry = FileEntry(labelframe, label="Dossier des orthomosaïques")

        self.src_pathentry.pack(expand=0, fill=tk.X)
        self.dest_pathentry.pack(expand=0, fill=tk.X)
        self.orthomosaic_pathentry.pack(expand=0, fill=tk.X)

        status_frame = ttk.LabelFrame(labelframe, text="Statut", padding="5px")
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
        flou_checkbox = ttk.Checkbutton(flou_frame, text="Appliquer le flou", variable=self.flou_var, command=toggle_blur_entry)
        flou_checkbox.pack(expand=0, fill=tk.X)

        file_tree_frame = ttk.Frame(self.root)
        file_tree_frame.pack(side=tk.BOTTOM, expand=1, fill=tk.BOTH, padx=5, pady=5)
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

    def open_add_index_window(self):

        def on_select(indices):
            print(f"Indices selectionnés : {indices}")

        AddIndexWindow(self.root, on_select)


def main():
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == '__main__':
    main()
