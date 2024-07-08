from tkinter import *
 
def quitter():
    fen = Toplevel(root)
    fen.grab_set()
    fen.focus_set()
    b = Button(fen, text = "Ok", command = root.quit).pack()
 
root = Tk()
bouton = Button(root, text = "quitter", command=quitter).pack()
root.mainloop()