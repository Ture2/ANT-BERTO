from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as tkmb
from tkinter.ttk import Progressbar, Separator
from functools import partial

import constants
import gui_controller

button_headers = ["Full", ".Sol", ".Hex"]
grid_headers = ["Herramienta", "Tipo", "Efectividad", "Seleccionada"]
sol_check = ["1", "0", "1", "0", "0", "0", "0", "1", "1", "1", "1", "0"]
hex_check = ["0", "1", "0", "1", "1", "1", "1", "0", "0", "0", "0", "1"]
full_check = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]
tools_length = len(constants.TOOLS)

table_row_start = 4


class MainGuiApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.elements = []
        self.tool_checkboxes = []
        self.file_paths = []
        self.progress = 0
        self.parent.title("ANT-BERTO")
        self.parent.resizable(True, True)
        self.parent.geometry("700x800")
        self.grid(sticky=N + S + W + E)
        self.__create_header(self.parent)
        self.__create_list(self.parent)
        self.__create_progress_bar(self.parent)
        self.__create_table(self.parent)

        self.buttonForget = Button(self.parent, text='Address contract', command=lambda: self.__hide())
        self.buttonRecover = Button(self.parent, text='Local contract', command=lambda: self.__show())
        self.buttonForget.grid(column=2, row=0, padx=10, pady=10, sticky=W + E)
        self.buttonRecover.grid(column=3, row=0, padx=10, pady=10, sticky=W + E)

    def __hide(self):
        self.file_list.grid_remove()

    def __show(self):
        self.file_list.grid()

    def __create_header(self, parent):
        sep = Separator(parent, orient=HORIZONTAL)
        sep.grid(row=1, column=0, columnspan=6, sticky=W + E)
        label = Label(parent, text="Seleccione un tipo de analisis", width=20).grid(row=2, column=0, columnspan=2, pady=10)
        self.elements.append(label)
        for i in range(0, len(button_headers)):
            __full_option = partial(self.__full_option, i)
            button = Button(parent, text=button_headers[i], command=__full_option, width=10,
                   activebackground='red').grid(row=2, column=i + 2, padx=5, pady=5)
            self.elements.append(button)



    def __create_table(self, parent):
        for i in range(0, len(grid_headers)):
            Label(parent, text=grid_headers[i]).grid(row=table_row_start - 1, column=i + 1)

        for i in range(0, tools_length):
            tool_type = constants.TOOLS_PROPERTIES[i].get("ext")
            Label(parent, text=constants.TOOLS[i]).grid(row=i + table_row_start, column=1)
            if tool_type == ".sol":
                Label(parent, text="Solidity").grid(row=i + table_row_start, column=2)
            else:
                Label(parent, text="Bytecode").grid(row=i + table_row_start, column=2)
            var = IntVar()
            Label(parent, text="Pendiente de añadir").grid(row=i + table_row_start, column=3)
            Checkbutton(parent, variable=var).grid(row=i + table_row_start, column=4)
            self.tool_checkboxes.append(var)

    def __create_list(self, parent):
        Label(parent, text="Añadir contrato:").grid(row=tools_length + table_row_start, column=2, sticky=W + E,
                                                    pady=10)
        Button(parent, text="Buscar", command=self.__open_file_dialog, width=15).grid(row=tools_length + table_row_start, column=3,
                                                                                      sticky=W + E)
        self.file_list = Listbox(parent, width=20)
        self.file_list.grid(row=tools_length + table_row_start + 1, column=2, columnspan=2, sticky=W + E)

        Label(parent, text='Para borrar un elemento seleccionelo \n de la lista y pulse el botón "borrar"').grid(
            row=tools_length + table_row_start + 2, column=2, columnspan=2, sticky=W + E, pady=10)
        Button(parent, text="Eliminar seleccionados", command=self.__open_file_dialog, width=20).grid(
            row=tools_length + table_row_start + 3, column=2, sticky=W)
        Button(parent, text="Eliminar todos", command=self.__open_file_dialog, width=20).grid(
            row=tools_length + table_row_start + 4, column=3, sticky=W + E)

    def __open_file_dialog(self):
        filename = filedialog.askopenfilename(
            filetypes=(("Solidity files", "*.sol"), ("Bytecode files", "*.bin;*.hex")
                       , ("All files", "*.*")))
        if filename != '':
            self.file_paths.append(str(filename))
            self.file_list.insert(END, str(filename).split('/')[-1])

    def __open_address_smartcontract(self):
        return 0

    def __create_progress_bar(self, parent):
        Label(parent, text="Progreso:").grid(row=tools_length + table_row_start + 4, column=2, sticky=W + E, pady=15)
        Progressbar(parent, orient=HORIZONTAL,
                                    length=constants.PROGRESS_BAR_LEN, variable=self.progress, mode='determinate').grid(
            row=tools_length + table_row_start + 4, column=3, columnspan=2, sticky=W, pady=15)
        Button(parent, text="Analizar", borderwidth=0, relief=SUNKEN, command=self.__analyse, width=10).grid(
            row=tools_length + table_row_start + 3, column=2, columnspan=2, sticky=W + E)

    def __full_option(self, i):
        if i == 0:
            for i in range(0, len(self.tool_checkboxes)):
                self.tool_checkboxes[i].set(full_check[i])
        elif i == 1:
            for i in range(0, len(self.tool_checkboxes)):
                self.tool_checkboxes[i].set(sol_check[i])
        else:
            for i in range(0, len(self.tool_checkboxes)):
                self.tool_checkboxes[i].set(hex_check[i])

    def __analyse(self):
        code = 0
        tool_check = False
        for i in range(0, len(self.tool_checkboxes)):
            if self.tool_checkboxes[i].get():
                tool_check = True
                break
        if tool_check and len(self.file_paths) > 0:
            results, code = gui_controller.start_analysis(self.file_paths, self.tool_checkboxes, self.progress, self.parent)
        else:
            tkmb.showinfo(message="Debe seleccionar al menos una herramienta y elegir un contrato", title="Error al introducir los datos")
        if code == 200:
            tkmb.showinfo(message="Informative message")


if __name__ == "__main__":
    root = Tk()
    MainGuiApplication(root)
    root.mainloop()
