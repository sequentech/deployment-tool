import tkinter as tk;
from tkinter import *
import json;
import file_manager as fm;

#Cargamos los ficheros de configuración
with open('config.json') as data_file:
    data = json.load(data_file)
with open('repos_config.json') as repos_data_file:
    repos_data = json.load(repos_data_file)

repos_vars = {}


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        #Creamos el botón de modificar repos.yml.
        self.modify = tk.Button(self)
        self.modify["text"] = "Modify repos.yml"
        self.modify["command"] = self.modify_files
        self.modify.pack(side="bottom")

        #Añadimos un pequeño espacio entre el botón y las checkboxes
        self.w = Canvas(self, width=10, height=20)
        self.w.pack(side="bottom")
        self.pack()

        #Añadimos las checkboxes de los módulos de repos
        for key in repos_data.keys():
            repos_vars[key] = IntVar();
            self.add_checkbox(key, repos_data[key])

    #Añade una checkbox con el nombre especificado en repos_config
    def add_checkbox(self, name, repo):
        self.checkbox = tk.Checkbutton(self, text="Enable " + name, variable=repos_vars[name])
        self.checkbox.pack(side="top")

    #Modificamos repos llamando a file_manager, enviándole el contenido de las checkboxes
    def modify_files(self):
        fm.modify_repos(repos_vars)


root = tk.Tk()
root.title("Agora-Voting Repos.yml configurator")
app = Application(master=root)
app.mainloop()