import tkinter as tk
from tabulate import tabulate
import td

class GUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("800x450")
        self.title("PySwissSys")
        self.tnmt = td.Tournament()
        self.tnmt.add_player(td.Player("Hari", 1900))
        self.tnmt.add_player(td.Player("d", 1930))
        self.setup_menu()
        self.new_tournament()

    def setup_menu(self):
        self.menu = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="New")
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.config(menu=self.menu)

    def new_tournament(self):
        self.table = tk.Text(self)
        self.table.insert(tk.END, tabulate(self.tnmt.table, headers='keys'))
        print(tabulate(self.tnmt.table, headers='keys'))
        self.table.place(x = 8, y = 8)       

if __name__ == '__main__':
    GUI().mainloop()
    