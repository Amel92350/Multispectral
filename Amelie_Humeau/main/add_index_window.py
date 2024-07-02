import os
import tkinter as tk
from tkinter import ttk, messagebox

class AddIndexWindow:
    def __init__(self, parent, on_select):
        self.parent = parent
        self.on_select = on_select
        self.top = tk.Toplevel(parent)
        self.top.title("Ajouter un Indice")
        self.top.geometry("300x200")
        self.calc_dir = self.get_calc_dir()


        self.init_widgets()

    def get_calc_dir(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        calc_dir = os.path.join(root_dir,'main','calculs')
        return calc_dir

    def init_widgets(self):
        label = ttk.Label(self.top, text="Sélectionnez un indice à ajouter")
        label.pack(pady=10)

        self.checkboxes = []
        self.selected_indices = []

        try:
            self.load_indices()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des indice : {str(e)}")

        add_frame = ttk.Frame(self.top)
        add_frame.pack(side=tk.BOTTOM,pady=10)

        nom_frame = ttk.Frame(add_frame)
        nom_frame.pack(pady=10)
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

        button_frame = ttk.Frame(self.top)
        button_frame.pack(side=tk.BOTTOM,pady=10)

        ok_button = ttk.Button(button_frame, text="OK", command=self.on_ok)
        ok_button.pack(side=tk.LEFT, padx=5)

        

        cancel_button = ttk.Button(button_frame, text="Annuler", command=self.top.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def load_indices(self):
    
        if not os.path.exists(self.calc_dir):
            raise FileNotFoundError(f"Le dossier '{self.calc_dir}' n'existe pas.")
        
        for filename in os.listdir(self.calc_dir):
            if filename.endswith(".txt"):
                index_name = filename.replace("_"," ").replace(".txt","")
                var = tk.BooleanVar(value=True)
                checkbox = ttk.Checkbutton(self.top,text=index_name,variable=var)
                checkbox.pack(anchor=tk.W)
                self.checkboxes.append((index_name,var))

    def on_add(self):
        
        calcul = self.calcul_entry.get()
        name = self.name_entry.get()
        filename = name.replace(' ','_')
        fichier = open(os.path.join(self.calc_dir,f"{filename}.txt"),"a")
        fichier.write(calcul)
        fichier.close()
        calcul = self.calcul_entry.get()
        var = tk.BooleanVar(value=True)
        checkbox = ttk.Checkbutton(self.top,text=name,variable=var)
        checkbox.pack(anchor=tk.W)
        self.checkboxes.append((name,var))
        

    def on_ok(self):
        self.selected_indices = [index_name for index_name,var in self.checkboxes if var.get()]
        if self.selected_indices:
            self.on_select(self.selected_indices)
            self.top.destroy()
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un indice à ajouter.")
