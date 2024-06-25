import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from threading import Thread
import os
import indice
import Correction as correction
import rescale
import tri
import stitch
import histogramme as h
from PIL import Image, ImageTk
import shutil
from file_tree_viewer import FileTreeApp

class FileEntry(ttk.Frame):
    """
    Classe permettant l'entrée d'un dossier avec une Entry et un bouton pour parcourir les dossiers.
    """
    def __init__(self, master=None, **kw):
        super().__init__(master)
        self.init_widgets(**kw)

    def init_widgets(self, **kw):
        """
        Initialise les widgets de la classe FileEntry.
        """
        self.label = ttk.Label(
            self,
            text=kw.get(
                "label",
                "Veuillez sélectionner le dossier des images : "
            )
        )
        self.folder_path = tk.StringVar()
        self.entry = ttk.Entry(
            self,
            textvariable=self.folder_path
        )
        self.button = ttk.Button(
            self,
            text="Parcourir",
            command=self.slot_browse,
            underline=0
        )

        self.label.pack(side=tk.TOP, expand=0, fill=tk.X)
        self.entry.pack(side=tk.LEFT, expand=1, fill=tk.X)
        self.button.pack(side=tk.LEFT, expand=0, fill=tk.NONE, padx=5)

    def slot_browse(self, tk_event=None, *args, **kw):
        """
        Ouvre une boîte de dialogue pour sélectionner un dossier.
        """
        _fpath = filedialog.askdirectory()
        self.folder_path.set(_fpath)

    def get_path(self):
        """
        Retourne le chemin du dossier sélectionné.
        """
        return self.folder_path.get()

class ImageProcessor:
    """
    Classe pour traiter les images en fonction des différents processus définis.
    """
    def __init__(self, src_pathentry, dest_pathentry, panorama_pathentry, status_label, progress_bar, flou_var, blur_value,tree):
        self.src_pathentry = src_pathentry
        self.dest_pathentry = dest_pathentry
        self.panorama_pathentry = panorama_pathentry
        self.status_label = status_label
        self.progress_bar = progress_bar
        self.processing = False
        self.cancelled = False
        self.flou_var = flou_var
        self.blur_value = blur_value
        self.tree=tree

    def is_processing(self):
        """
        Retourne True si un traitement est en cours.
        """
        return self.processing

   

    def start_processing(self, process_type):
        """
        Démarre le traitement des images en fonction du type de processus spécifié (full ou panoramas).
        """
        src_path = self.src_pathentry.get_path()
        dest_path = self.dest_pathentry.get_path()
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        apply_blur = self.flou_var.get()
        panorama_path = self.panorama_pathentry.get_path()    

        if apply_blur:
            blur_value = int(self.blur_value.get())


        def process():
            """
            Fonction de traitement des images exécutée dans un thread séparé.
            """
            try:
                if process_type == "full":
                    new_src_path = os.path.join(src_path, "copied_images")
                    # Copie les images sources dans un nouveau dossier pour le traitement
                    if os.path.exists(new_src_path):
                        shutil.rmtree(new_src_path)
                    shutil.copytree(src_path, new_src_path)
                    self.processing = True
                    self.status_label.config(text="Correction en cours...")
                    self.progress_bar.start()
                    correction.main(os.path.join(new_src_path, "*"))

                    self.status_label.config(text="Tri en cours...")
                    tri.main(new_src_path, dest_path)
                    #h.main(dest_path+"/*")
                    

                self.processing = True
                self.status_label.config(text="Création des panoramas en cours...")
                self.progress_bar.start()
                stitch.main(dest_path)

                self.status_label.config(text="Redimensionnement en cours...")
                if apply_blur:
                    rescale.main(os.path.join(dest_path, "panoramas"), test=True, flou=blur_value)
                else:
                    rescale.main(os.path.join(dest_path, "panoramas"), test=True)
 
                self.status_label.config(text="Terminé.")
                self.progress_bar.stop()
                self.processing = False

                self.tree.update_base_path(os.path.join(dest_path, "panoramas"))
                messagebox.showinfo("Information", "Images traitées" if process_type == "full" else "Panoramas créés")
            
                
            
            except Exception as e:
                self.progress_bar.stop()
                self.processing = False
                messagebox.showerror("Erreur", str(e))

        Thread(target=process).start()

    def process_index(self, Ic):
        """
        Démarre le traitement d'indice spécifié.
        """
        panorama_path = self.panorama_pathentry.get_path()

        def process():
            """
            Fonction de traitement des indices exécutée dans un thread séparé.
            """
            try:
                self.processing = True
                self.status_label.config(text="Traitement des panoramas en cours...")
                self.progress_bar.start()

                

                indice.main(panorama_path, Ic)
                self.status_label.config(text="Egalisation en cours...")
                self.status_label.config(text="Traitement terminé.")
                self.progress_bar.stop()
                self.processing = False

                self.tree.update_base_path(panorama_path)

                if Ic == "text":
                    messagebox.showinfo("Information", "Indice de texture calculé.")
                elif Ic == "sal":
                    messagebox.showinfo("Information", "Indice de salinité calculé.")
                elif Ic == "org":
                    messagebox.showinfo("Information", "Indice de matière organique calculé.")
                elif Ic == "savi":
                    messagebox.showinfo("Information", "Indice de végétation calculé.")

                

            except Exception as e:
                self.progress_bar.stop()
                self.processing = False
                messagebox.showerror("Erreur", str(e))

        Thread(target=process).start()

    def cancel_processing(self):
        """
        Annule le traitement en cours.
        """
        self.cancelled = True

def init_root():
    """
    Initialise la fenêtre principale de l'application.
    """
    root = tk.Tk()
    root.title("Logiciel de traitement d'images multispectrales")
    root.geometry("1000x700")

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Fichier", menu=file_menu)

    labelframe = ttk.LabelFrame(
        root,
        text="Bienvenue",
        padding="5px"
    )

    src_pathentry = FileEntry(labelframe, label="Dossier source : ")
    dest_pathentry = FileEntry(labelframe, label="Dossier destination : ")
    panoramas_pathentry = FileEntry(labelframe, label="Dossier des panoramas")

    status_frame = ttk.LabelFrame(
        labelframe,
        text="Statut",
        padding="5px"
    )

    status_label = ttk.Label(status_frame, text="Prêt")
    status_label.pack(side=tk.LEFT, expand=1, fill=tk.X)

    progress_bar = ttk.Progressbar(status_frame, mode='indeterminate')
    progress_bar.pack(side=tk.LEFT, expand=1, fill=tk.X, padx=5)

    flou_frame = ttk.Frame(labelframe)
    flou_frame.pack(side=tk.TOP, expand=0, fill=tk.X, padx=5)

    flou_var = tk.BooleanVar()

    def toggle_blur_entry():
        """
        Affiche ou masque l'Entry pour la valeur du flou en fonction de l'état de la checkbox.
        """
        if flou_var.get():
            blur_entry.pack(side=tk.LEFT, expand=0, padx=5)
        else:
            blur_entry.pack_forget()

    blur_value = tk.StringVar()
    blur_entry = ttk.Entry(flou_frame, textvariable=blur_value)

    flou_checkbox = ttk.Checkbutton(
        flou_frame,
        text="Appliquer le flou",
        variable=flou_var,
        command=toggle_blur_entry
    )
    flou_checkbox.pack(expand=0, fill=tk.X)

    file_tree_frame = ttk.Frame(root)
    file_tree_frame.pack(side = tk.BOTTOM,expand=1,fill = tk.BOTH,padx=5,pady=5)
    file_tree_app = FileTreeApp(file_tree_frame)

    processor = ImageProcessor(src_pathentry, dest_pathentry, panoramas_pathentry, status_label, progress_bar, flou_var, blur_value,file_tree_app)

    def quit_app():
        """
        Quitte l'application si aucun traitement n'est en cours.
        """
        if not processor.is_processing():
            root.quit()
        else:
            messagebox.showinfo("Information", "Attendez que le traitement soit terminé avant de quitter.")

    file_menu.add_command(label="Quitter", command=quit_app)
    action_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Actions", menu=action_menu)
    action_menu.add_command(label="Lancer le traitement complet", command=lambda: processor.start_processing("full"))
    action_menu.add_command(label="Créer des panoramas", command=lambda: processor.start_processing("panoramas"))
    action_menu.add_command(label="Annuler", command=processor.cancel_processing)

    indice_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Indices", menu=indice_menu)
    indice_menu.add_command(label="Indice de texture des sols", command=lambda: processor.process_index("text"))
    indice_menu.add_command(label="Indice de salinité", command=lambda: processor.process_index("sal"))
    indice_menu.add_command(label="Indice de matière organique", command=lambda: processor.process_index("org"))
    indice_menu.add_command(label="Indice de végétation ajusté pour le sol", command=lambda: processor.process_index("savi"))

    src_pathentry.pack(expand=0, fill=tk.X)
    dest_pathentry.pack(expand=0, fill=tk.X)
    panoramas_pathentry.pack(expand=0, fill=tk.X)
    status_frame.pack(side=tk.BOTTOM, expand=1, fill=tk.X, padx=5, pady=5)
    labelframe.pack(side=tk.TOP, expand=1, fill=tk.BOTH, padx=5, pady=5)

    

    def update_file_tree_app(*args):
        dest_path = panoramas_pathentry.get_path()
        file_tree_app.update_base_path(dest_path)

    panoramas_pathentry.folder_path.trace_add("write",update_file_tree_app)
    
    ttk.Sizegrip(root).pack(side=tk.RIGHT, expand=0, fill=tk.Y, padx=5, pady=5)

    return root

def main():
    """
    Point d'entrée principal de l'application.
    """
    root = init_root()
    root.mainloop()

if __name__ == '__main__':
    main()
