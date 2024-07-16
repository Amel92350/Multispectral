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
import ortho_metashape as meta
import stitch 
import histogramme as h

class ImageProcessor:
    """
    Classe pour traiter les images en fonction des différents processus définis.
    """
    def __init__(self, src_pathentry, dest_pathentry,status_label, progress_bar, flou_var, blur_value, tree,method_value):
        self.src_pathentry = src_pathentry
        self.dest_pathentry = dest_pathentry
        self.status_label = status_label
        self.progress_bar = progress_bar
        self.processing = False
        self.flou_var = flou_var
        self.blur_value = blur_value
        self.tree = tree
        self.method_value = method_value

        # Configurer le logger
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def is_processing(self):
        """
        Retourne True si un traitement est en cours.
        """
        return self.processing

    def start_processing(self, process_type):
        """
        Démarre le traitement des images en fonction du type de processus spécifié (full, one, ou orthos).
        """
        if self.processing:
            messagebox.showwarning("Avertissement", "Un traitement est déjà en cours.")
            return

        try:
            self.validate_paths(process_type)
            apply_blur, blur_value = self.get_blur_values()
            method_value = self.method_value.get()

            # Démarrer le traitement dans un thread séparé
            Thread(target=self.process_images, args=(process_type, apply_blur, blur_value, method_value)).start()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            logging.error(str(e))

    def validate_paths(self, process_type):
        """
        Valide les chemins de source et de destination.
        """
        src_path = self.src_pathentry.get_path()
        dest_path = self.dest_pathentry.get_path()

        if process_type in ["full", "one"]:
            if not dest_path:
                raise ValueError("Le chemin destination est vide")
            if not os.path.exists(src_path):
                raise ValueError("Le chemin  est invalide")
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

        if not src_path:
            raise ValueError("Le chemin source est vide")
        if not os.path.exists(src_path):
                raise ValueError("Le chemin source est invalide")
        

    def get_blur_values(self):
        """
        Récupère les valeurs de flou.
        """
        apply_blur = self.flou_var.get()
        blur_value = int(self.blur_value.get()) if apply_blur else None

        if apply_blur and (blur_value is None or blur_value % 2 == 0):
            raise ValueError("La valeur de la médiane doit être un nombre impair.")
        
        return apply_blur, blur_value

    def process_images(self, process_type, apply_blur, blur_value, method_value):
        """
        Fonction de traitement des images exécutée dans un thread séparé.
        """
        self.processing = True
        start_time = time.time()
        src_path = self.src_pathentry.get_path()
        dest_path = self.dest_pathentry.get_path()

        try:
            if process_type in ["full", "one"]:
                self.process_full_or_one(process_type, blur_value)
                self.update_file_tree(os.path.join(dest_path))
            
            if process_type in ["full", "orthos"]:
                self.create_orthomosaics( blur_value, method_value,src_path if process_type=="orthos" else dest_path)

            elapsed_time = time.time() - start_time
            self.show_completion_message(process_type, elapsed_time)
        except Exception as e:
            logging.error("Erreur lors du traitement : %s", e)
            messagebox.showerror("Erreur", str(e))
        finally:
            self.processing = False
            self.progress_bar.stop()
            

    def process_full_or_one(self, process_type, blur_value):
        """
        Traite les images pour les processus 'full' ou 'one'.
        """
        src_path = self.src_pathentry.get_path()
        dest_path = self.dest_pathentry.get_path()

        #Copier les images dans un autre dossier pour éviter de faire le traitement sur les images originales
        new_src_path = os.path.join(src_path, "copied_images")
        if os.path.exists(new_src_path):
            shutil.rmtree(new_src_path)
        shutil.copytree(src_path, new_src_path)

        self.update_status("Correction en cours...", "Démarrage de la correction.")
        correction.main(new_src_path if process_type == "one" else new_src_path + "/*")
        
        self.update_status("Tri en cours...", "Démarrage du tri.")
        if process_type == "one":
            tri.one(new_src_path, dest_path)
            self.update_status("Alignement en cours...", "Démarrage de l'alignement.")
            rescale.main(os.path.join(dest_path, "orthos"), onedir=True, flou=blur_value, recadre=True)
        else:
            rescale.main(new_src_path + "/*")
            tri.main(new_src_path, dest_path)
            
    def create_orthomosaics(self, blur_value, method_value,path):
        """
        Crée des orthomosaïques à partir des images traitées en fonction de la méthode.
        """
        self.update_status("Création des orthomosaïques en cours...", "Démarrage de la création des orthomosaïques.")

        #On va lancer la méthode Stitch, Metashape ou Micmac en fonction du bouton coché.
        if method_value=="meta":
            meta.main(path)
        elif method_value=="stitch":
            stitch.main(path)
        elif method_value=="micmac":
            # TODO : Ici faire appel à la fonction principale de traitement d'un fichier micmac.py
            raise ValueError("Erreur, Micmac n'est pas initialisé")

        self.update_status("Alignement en cours...", "Démarrage de l'alignement.")
        rescale.main(os.path.join(path, "orthos"), onedir=True, flou=blur_value)
        
        self.update_file_tree(path)

    def update_status(self, status_message, log_message):
        """
        Met à jour l'état de la barre de progression et les messages de statut.
        """
        self.status_label.config(text=status_message)
        logging.info(log_message)
        self.progress_bar.start()

    def show_completion_message(self, process_type, elapsed_time):
        """
        Affiche un message de fin de traitement.
        """
        elapsed_minutes, elapsed_seconds = divmod(elapsed_time, 60)
        messagebox.showinfo(
            "Information",
            f"Images traitées en {int(elapsed_minutes)} minutes et {int(elapsed_seconds)} secondes."
            if process_type in ["full", "one"] else
            f"Orthomosaïques créées en {int(elapsed_minutes)} minutes et {int(elapsed_seconds)} secondes."
        )

    def update_file_tree(self,path):
        """
        Met à jour l'arborescence des fichiers.
        """
        self.tree.update_base_path(os.path.join(path, "orthos"))
