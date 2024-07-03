import os
import shutil
import time
import logging
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

        # Configurer le logger
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def is_processing(self):
        """
        Retourne True si un traitement est en cours.
        """
        return self.processing

    def start_processing(self, process_type):
        """
        Démarre le traitement des images en fonction du type de processus spécifié (full ou panoramas).
        """
        if self.processing:
            messagebox.showwarning("Avertissement", "Un traitement est déjà en cours.")
            return

        src_path = self.src_pathentry.get_path()
        dest_path = self.dest_pathentry.get_path()
        
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        
        apply_blur = self.flou_var.get()
        blur_value = int(self.blur_value.get()) if apply_blur else None

        def process():
            """
            Fonction de traitement des images exécutée dans un thread séparé.
            """
            logging.info("Démarrage du processus de traitement des images.")
            start_time = time.time()
            self.processing = True
            self.cancelled = False
            try:
                if process_type == "full":
                    new_src_path = os.path.join(src_path, "copied_images")
                    # Copie les images sources dans un nouveau dossier pour le traitement
                    if os.path.exists(new_src_path):
                        shutil.rmtree(new_src_path)
                    shutil.copytree(src_path, new_src_path)
                    
                    self.status_label.config(text="Correction en cours...")
                    self.progress_bar.start()
                    logging.info("Démarrage de la correction.")
                    correction.main(os.path.join(new_src_path, "*"))

                    self.status_label.config(text="Tri en cours...")
                    logging.info("Démarrage du tri.")
                    tri.main(new_src_path, dest_path)

                if process_type != "full":
                    self.progress_bar.start()
                    
                self.status_label.config(text="Création des orthomosaïques en cours...")
                logging.info("Démarrage de la création des orthomosaïques.")
                meta.main(dest_path)

                self.status_label.config(text="Alignement en cours...")
                logging.info("Démarrage de l'alignement.")
                if apply_blur:
                    rescale.main(os.path.join(dest_path, "orthos"), test=True, flou=blur_value)
                else:
                    rescale.main(os.path.join(dest_path, "orthos"), test=True)

                self.status_label.config(text="Terminé.")
                self.progress_bar.stop()
                logging.info("Traitement terminé.")
                elapsed_time = time.time() - start_time
                elapsed_minutes, elapsed_seconds = divmod(elapsed_time, 60)
                messagebox.showinfo(
                    "Information",
                    f"Images traitées en {int(elapsed_minutes)} minutes et {int(elapsed_seconds)} secondes."
                    if process_type == "full" else
                    f"Orthomosaïques créées en {int(elapsed_minutes)} minutes et {int(elapsed_seconds)} secondes."
                )
            except Exception as e:
                logging.error("Erreur lors du traitement : %s", e)
                messagebox.showerror("Erreur", str(e))
            finally:
                self.progress_bar.stop()
                self.processing = False

            self.tree.update_base_path(os.path.join(dest_path, "orthos"))

        Thread(target=process).start()

    def process_index(self, Ic):
        """
        Démarre le traitement d'indice spécifié.
        """
        if self.processing:
            messagebox.showwarning("Avertissement", "Un traitement est déjà en cours.")
            return

        orthomosaic_path = self.orthomosaic_pathentry.get_path()

        def process():
            """
            Fonction de traitement des indices exécutée dans un thread séparé.
            """
            logging.info("Démarrage du processus de calcul des indices.")
            self.processing = True
            self.cancelled = False
            try:
                self.status_label.config(text="Calculs en cours...")
                self.progress_bar.start()

                indice.main(orthomosaic_path, Ic)
                self.status_label.config(text="Traitement terminé.")
                logging.info("Calcul des indices terminé.")
                message = {
                    "text": "Indice de texture calculé.",
                    "sal": "Indice de salinité calculé.",
                    "org": "Indice de matière organique calculé.",
                    "savi": "Indice de végétation calculé."
                }.get(Ic, "Traitement d'indice terminé.")

                messagebox.showinfo("Information", message)
            except Exception as e:
                logging.error("Erreur lors du calcul des indices : %s", e)
                messagebox.showerror("Erreur", str(e))
            finally:
                self.progress_bar.stop()
                self.processing = False

            self.tree.update_base_path(orthomosaic_path)

        Thread(target=process).start()

    def cancel_processing(self):
        """
        Annule le traitement en cours.
        """
        self.cancelled = True
        logging.info("Annulation du traitement en cours.")
