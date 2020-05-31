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
efectivity_array = ["50", "80", "40", "60", "80", "70", "80", "90", "60", "65", "70", "80"]
tools_length = len(constants.TOOLS)

table_row_start = 4


class ResultsFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.window = Toplevel(parent)

    def close(self):
        self.window.destroy()


class MainGuiApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.elements = []
        self.tool_checkboxes = []
        self.file_paths = []
        self.is_local_analysis = True
        self.is_one_result_open = False
        self.progress = 0
        self.parent.title("ANT-BERTO")
        self.parent.resizable(True, True)
        self.parent.geometry("700x800")
        self.grid(sticky=N + S + W + E)
        self.__create_header(self.parent)
        self.__create_list(self.parent)
        self.__create_address_entry(self.parent)
        self.__create_progress_bar(self.parent)
        self.__create_table(self.parent)

        self.buttonForget = Button(self.parent, text='Address contract', command=lambda: self.__hide())
        self.buttonRecover = Button(self.parent, text='Local contract', command=lambda: self.__show())
        self.buttonForget.grid(column=2, row=0, padx=10, pady=10, sticky=W + E)
        self.buttonRecover.grid(column=3, row=0, padx=10, pady=10, sticky=W + E)

    def __hide(self):
        self.is_local_analysis = False
        self.file_list.grid_remove()
        for e in self.elements_to_hide:
            e.grid()
        for e in self.elements_to_show:
            e.grid_remove()

    def __show(self):
        self.is_local_analysis = True
        for e in self.elements_to_hide:
            e.grid_remove()
        for e in self.elements_to_show:
            e.grid()
        self.file_list.grid()

    def __create_header(self, parent):
        sep = Separator(parent, orient=HORIZONTAL)
        sep.grid(row=1, column=0, columnspan=6, sticky=W + E)
        label = Label(parent, text="Seleccione un tipo de analisis", width=20).grid(row=2, column=0, columnspan=2,
                                                                                    pady=10)
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
            Label(parent, text=efectivity_array[i]).grid(row=i + table_row_start, column=3)
            Checkbutton(parent, variable=var).grid(row=i + table_row_start, column=4)
            self.tool_checkboxes.append(var)

    def __create_list(self, parent):
        self.elements_to_show = []
        self.lbl = Label(parent, text="Añadir contrato:")
        self.btn = Button(parent, text="Buscar", command=self.__open_file_dialog, width=15)
        self.file_list = Listbox(parent, width=20)
        self.ins = Label(parent,
                         text='Para borrar un elemento seleccionelo \n de la lista y pulse el botón "borrar"')

        self.lbl.grid(row=tools_length + table_row_start, column=2, sticky=W + E, pady=10)
        self.btn.grid(row=tools_length + table_row_start, column=3, sticky=W + E)
        self.file_list.grid(row=tools_length + table_row_start + 1, column=2, columnspan=2, sticky=W + E)
        self.ins.grid(row=tools_length + table_row_start + 2, column=2, columnspan=2, sticky=W + E, pady=10)

        self.elements_to_show.append(self.lbl)
        self.elements_to_show.append(self.btn)
        self.elements_to_show.append(self.file_list)
        self.elements_to_show.append(self.ins)

        Button(parent, text="Eliminar seleccionados", command=self.__open_file_dialog, width=20).grid(
            row=tools_length + table_row_start + 3, column=2, sticky=W)
        Button(parent, text="Eliminar todos", command=self.__open_file_dialog, width=20).grid(
            row=tools_length + table_row_start + 4, column=3, sticky=W + E)

    def __create_address_entry(self, parent):
        self.elements_to_hide = []
        self.entry_address = Entry()
        self.address_txt = Label(parent, text='Inserte una dirección de un \ncontrato inteligente y pulse analizar')

        self.address_txt.grid(row=tools_length + table_row_start, column=2, columnspan=2, sticky=W + E, pady=10)
        self.entry_address.grid(row=tools_length + table_row_start + 1, column=2, columnspan=2, sticky=W + E,
                                pady=(5, 25))

        self.elements_to_hide.append(self.entry_address)
        self.elements_to_hide.append(self.address_txt)

        for e in self.elements_to_hide:
            e.grid_remove()

    def __open_file_dialog(self):
        filename = filedialog.askopenfilename(
            filetypes=(("Solidity files", "*.sol"), ("Bytecode files", "*.hex")
                       , ("All files", "*.*")))
        if filename != '':
            self.file_paths.append(str(filename))
            self.file_list.insert(END, str(filename).split('/')[-1])

    def __open_address_smartcontract(self):
        self.entry_address.get()

    def __create_progress_bar(self, parent):
        Label(parent, text="Progreso:").grid(row=tools_length + table_row_start + 4, column=2, sticky=W + E, pady=15)
        Progressbar(parent, orient=HORIZONTAL,
                    length=constants.PROGRESS_BAR_LEN, variable=self.progress, mode='determinate').grid(
            row=tools_length + table_row_start + 4, column=3, columnspan=2, sticky=W, pady=15)
        Button(parent, text="Analizar", borderwidth=0, relief=SUNKEN, command=self.__new_window, width=10).grid(
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
        if (tool_check and len(self.file_paths) > 0) or (not self.is_local_analysis and tool_check):
            results, code = gui_controller.start_analysis(self.file_paths, self.tool_checkboxes, self.is_local_analysis,
                                                          self.entry_address.get())
        else:
            tkmb.showinfo(message="Debe seleccionar al menos una herramienta y elegir un contrato",
                          title="Error al introducir los datos")
        if code == 200:
            tkmb.showinfo(message="Informative message")

    def __new_window(self):
        if not self.is_one_result_open:
            self.results_window = ResultsFrame(root)
            self.is_one_result_open = True
        else:
            self.results_window.close()
            self.results_window = ResultsFrame(root)


if __name__ == "__main__":
    root = Tk()
    MainGuiApplication(root)
    root.mainloop()
