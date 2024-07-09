import os
import tkinter as tk
from tkinter import ttk, messagebox
import re
from tkscrolledframe import ScrolledFrame  # Import ScrolledFrame

class AddCalculWindow:


    """
    Fenêtre d'affichage pour ajouter un calcul ou en appliquer
    """
    def __init__(self, parent, on_select, mode):
        self.parent = parent
        self.on_select = on_select
        self.top = tk.Toplevel(parent)
        self.top.grab_set()
        self.top.focus_set()
        self.top.title("Calculs")
        self.width = 500
        self.top.geometry("600x500")
        self.calc_dir = self.get_calc_dir()
        self.mode = mode

        self.init_styles()
        self.init_widgets(mode)

    def get_calc_dir(self):
        """
        Retourne le chemin absolu du dossier contenant les fichiers texte
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        calc_dir = os.path.join(root_dir, 'main', 'calculs')
        return calc_dir

    def init_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TEntry", font=("Helvetica", 10))
        style.configure("TCheckbutton", font=("Helvetica", 10))

    def init_widgets(self, mode):
        if mode == "applique":
            label = ttk.Label(self.top, text="Sélectionnez un ou plusieurs calculs à appliquer")
            label.pack(pady=10)

            # Use ScrolledFrame for checkboxes
            sf = ScrolledFrame(self.top)
            sf.pack(expand=True, fill='both')

            # Create a fixed frame within ScrolledFrame for actual content
            inner_frame = sf.display_widget(ttk.Frame)

            self.checkboxes_frame = ttk.Frame(inner_frame)
            self.checkboxes_frame.pack(expand=True, fill=tk.X)

            self.checkboxes = []
            self.selected_indices = []

            try:
                self.load_indices()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement des calculs : {str(e)}")

            button_frame = ttk.Frame(self.top)
            button_frame.pack(side=tk.BOTTOM, pady=10)

            ok_button = ttk.Button(button_frame, text="OK", command=self.on_ok)
            ok_button.pack(side=tk.LEFT, padx=5)

            cancel_button = ttk.Button(button_frame, text="Annuler", command=self.top.destroy)
            cancel_button.pack(side=tk.LEFT, padx=5)


        elif mode == "add":
            add_frame = ttk.Frame(self.top)
            add_frame.pack(pady=10, fill=tk.X)

            nom_frame = ttk.Frame(add_frame)
            nom_frame.pack(pady=10, fill=tk.X)
            name_label = ttk.Label(nom_frame, text="Nom : ")
            name_label.pack(side=tk.LEFT, padx=5)

            self.name_entry = ttk.Entry(nom_frame)
            self.name_entry.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)

            calcul_frame = ttk.Frame(add_frame)
            calcul_frame.pack(pady=5, fill=tk.X)

            calcul_label = ttk.Label(calcul_frame, text="Calcul =")
            calcul_label.pack(side=tk.LEFT, padx=5)

            self.calcul_entry = ttk.Entry(calcul_frame)
            self.calcul_entry.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)

            add_button = ttk.Button(add_frame, text="Ajouter", command=self.on_add)
            add_button.pack(side=tk.LEFT, padx=5)

    def check_calcul(self, calcul: str) -> bool:
        """
        Vérifie que le calcule correspond à la norme définie 
        norme : les constantes correspondent aux différente bande et les opérations +-*/
        """
        constantes = ["415nm", "450nm", "570nm", "675nm", "730nm", "850nm"]
        constantes_regex = '|'.join(re.escape(c) for c in constantes)

        const_or_expr = rf'(?:{constantes_regex}|\([^()]*\))'
        expression_regex = re.compile(rf'^\s*{const_or_expr}(?:\s*[-+*/]\s*{const_or_expr})*\s*$')

        return bool(expression_regex.match(calcul))

    def load_indices(self):
        """
        Charge les fichiers texte pour les afficher dans la fenêtre
        """
        if not os.path.exists(self.calc_dir):
            raise FileNotFoundError(f"Le dossier '{self.calc_dir}' n'existe pas.")
        
        for filename in os.listdir(self.calc_dir):
            if filename.endswith(".txt"):
                index_name = filename.replace("_", " ").replace(".txt", "")

                var = tk.BooleanVar(value=True)

                frame = ttk.Frame(self.checkboxes_frame)  # Use checkboxes_frame for checkboxes
                frame.pack(anchor=tk.W, expand=True,fill=tk.X,padx=5,pady=5)

                checkbox = ttk.Checkbutton(frame, text=index_name, variable=var)
                checkbox.pack(anchor=tk.W,side=tk.LEFT, fill=tk.X, expand=True)  # Ensure Checkbutton fills horizontally

                delete_button = ttk.Button(frame, text="❌", command=lambda name=index_name: self.on_delete(name))
                delete_button.pack(side=tk.RIGHT, padx=5)  # Adjust padding for the delete button

                self.checkboxes.append((index_name, var,frame))

    def on_add(self):
        """
        Méthode pour ajouter un nouveau calcul c'est à dire créer un fichier texte
        """
        calcul = self.calcul_entry.get()
        if self.check_calcul(calcul):
            name = self.name_entry.get()
            filename = name.replace(' ', '_')
            if os.path.exists(os.path.join(self.calc_dir, f"{filename}.txt")):

                with open(os.path.join(self.calc_dir, f"{filename}.txt"), "w") as fichier:
                    fichier.write(calcul)
            else:
                with open(os.path.join(self.calc_dir, f"{filename}.txt"), "a") as fichier:
                    fichier.write(calcul)

            self.top.destroy()
            messagebox.showinfo("Succès", "Calcul ajouté avec succès.")
        else:
            messagebox.showwarning("Avertissement", "L'expression n'est pas valide, exemple d'expression correcte : '450nm+415nm'")

    def on_ok(self):
        """
        Lance la fonction on_select de la classe MainApplication pour appliquer les indices selecitonnés
        """
        self.selected_indices = [index_name for index_name, var, frame in self.checkboxes if var.get()]
        for i in range(len(self.selected_indices)):
            filename = self.selected_indices[i].replace(' ','_') +".txt"
            filepath = os.path.join(self.calc_dir,filename)
            self.selected_indices[i] = filepath
        if self.selected_indices:
            self.on_select(self.selected_indices)
            self.top.destroy()
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un calcul à appliquer.")
            
    def on_delete(self, name):
        """
        Permet de supprimer un fichier texte
        """
        filename = name.replace(' ', '_') + ".txt"
        filepath = os.path.join(self.calc_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            for index_name, var, frame in self.checkboxes:
                if index_name == name:
                    frame.destroy()
                    self.checkboxes.remove((index_name, var, frame))
                    break
        else:
            messagebox.showerror("Erreur", f"Le fichier '{filename}' n'existe pas.")

if __name__ == "__main__":
    root = tk.Tk()
    test = AddCalculWindow(root, None, "applique")
    root.mainloop()
