import os
import shutil
import time
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import correction 
import rescale
import tri
import test_metashape as meta
import indice

class ImageProcessor:
    """
    Classe pour traiter les images en fonction des différents processus définis.
    """
    def __init__(self, src_pathentry, dest_pathentry, orthomosaic_pathentry, status_label, progress_bar, flou_var, blur_value, tree):
        self.src_pathentry = src_pathentry
        self.dest_pathentry = dest_pathentry
        self.orthomosaic_pathentry = orthomosaic_pathentry
        self.status_label = status_label
        self.progress_bar = progress_bar
        self.processing = False
        self.cancelled = False
        self.flou_var = flou_var
        self.blur_value = blur_value
        self.tree = tree

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

        if apply_blur:
            blur_value = int(self.blur_value.get())

        def process():
            """
            Fonction de traitement des images exécutée dans un thread séparé.
            """
            start_time = time.time()
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
                    # h.main(dest_path+"/*")

                self.processing = True
                self.status_label.config(text="Création des orthomosaïques en cours...")
                self.progress_bar.start()
                meta.main(dest_path)

                self.status_label.config(text="Alignement en cours...")
                if apply_blur:
                    rescale.main(os.path.join(dest_path, "orthos"), test=True, flou=blur_value)
                else:
                    rescale.main(os.path.join(dest_path, "orthos"), test=True)

                self.status_label.config(text="Terminé.")
                self.progress_bar.stop()
                self.processing = False

                self.tree.update_base_path(os.path.join(dest_path, "orthos"))
                elapsed_time = time.time() - start_time
                elapsed_minutes, elapsed_seconds = divmod(elapsed_time, 60)
                messagebox.showinfo(
                    "Information",
                    f"Images traitées en {int(elapsed_minutes)} minutes et {int(elapsed_seconds)} secondes."
                    if process_type == "full" else
                    f"Orthomosaïques créées en {int(elapsed_minutes)} minutes et {int(elapsed_seconds)} secondes."
                )

            except Exception as e:
                self.progress_bar.stop()
                self.processing = False
                messagebox.showerror("Erreur", str(e))

        Thread(target=process).start()

    def process_index(self, Ic):
        """
        Démarre le traitement d'indice spécifié.
        """
        orthomosaic_path = self.orthomosaic_pathentry.get_path()

        def process():
            """
            Fonction de traitement des indices exécutée dans un thread séparé.
            """
            try:
                self.processing = True
                self.status_label.config(text="Calculs en cours...")
                self.progress_bar.start()

                indice.main(orthomosaic_path, Ic)
                self.status_label.config(text="Egalisation en cours...")
                self.status_label.config(text="Traitement terminé.")
                self.progress_bar.stop()
                self.processing = False

                self.tree.update_base_path(orthomosaic_path)

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
