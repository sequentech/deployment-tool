import tkinter as tk;
from tkinter import *
import json;
import file_manager as fm;

#Cargamos los ficheros de configuración
with open('provision_config.json') as provision_data_file:
    provis_data = json.load(provision_data_file)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        #Creamos el botón que reemplaza los archivos de configuración
        self.modify = tk.Button(self)
        self.modify["text"] = "Modify provision configuration"
        self.modify["command"] = self.modify_files
        self.modify.pack(side="bottom")

        #Listbox para elegir el tipo de servidor
        self.listbox = Listbox()
        self.listbox.pack()
        self.servers = provis_data["servers"]
        for item in self.servers:
            self.listbox.insert(END, item)

        #Checkbox para indicar si es un provision base
        self.is_base = IntVar();
        self.checkbox = tk.Checkbutton(self, text="Base provisioning", variable=self.is_base)
        self.checkbox.pack(side="top")

        self.pack()

    #Función para modificar los archivos de provision
    def modify_files(self):
        server = self.listbox.curselection()
        server = [self.servers[int(item)] for item in server][0]
        fm.modify_provision(server, self.is_base)

root = tk.Tk()
root.title("Agora-Voting Provision configurator")
app = Application(master=root)
app.mainloop()