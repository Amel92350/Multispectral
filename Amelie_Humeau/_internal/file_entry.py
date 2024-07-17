import tkinter as tk
from tkinter import ttk, filedialog

class FileEntry(ttk.Frame):
    """
    Classe permettant l'entrée d'un dossier avec une Entry et un bouton pour Parcourir"""

    def __init__(self, master=None, **kw):
        super().__init__(master)
        self.init_widgets(**kw)

    def init_widgets(self, **kw):
        """
        Initialise les widgets de la classe FileEntry.
        """
        self.label = ttk.Label(self, text=kw.get("label", "Veuillez sélectionner le dossier des images : "))
        self.folder_path = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.folder_path)
        self.button = ttk.Button(self, text="Parcourir", command=self.slot_browse, underline=0)

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