import tkinter as tk
from tabulate import tabulate
import td

class GUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("800x450")
        self.title("PySwissSys")
        self.tnmt = td.Tournament()
        # self.tnmt.add_player(td.Player("Hari", 1900))
        # self.tnmt.add_player(td.Player("d", 1930))
        self.setup_menu()
        self.update_standings()

    def setup_menu(self):
        self.menu = tk.Menu(self)
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="New")
        reg_menu = tk.Menu(self.menu, tearoff=0)
        reg_menu.add_command(label = 'Register', command=self.add_player)
        self.menu.add_cascade(label='File', menu=file_menu)
        self.menu.add_cascade(label='Players', menu = reg_menu)
        self.config(menu=self.menu)
    
    def add_player(self):

        def register():
            self.tnmt.add_player(td.Player(name.get(), uscf_rating.get(), uscf_id = uscf_id.get()))
            self.update_standings()
            win.destroy()

        win = tk.Toplevel()
        win.wm_title("Registration")
        win.geometry("400x200")
        name = tk.Entry(win, width=30)
        uscf_id = tk.Entry(win, width=30)
        uscf_rating = tk.Entry(win, width=30)
        labels = ("Name", "USCF ID", "USCF Rating")
        entries = [name, uscf_id, uscf_rating]
        spacing = [0.1, 0.25, 0.4]
        for i in range(len(spacing)):
            tk.Label(win, text=f"{labels[i]}: ").place(relx=0.05, rely=spacing[i], anchor="w")
            entries[i].place(relx = 0.5, rely = spacing[i], anchor=tk.CENTER)

        submit = tk.Button(win, text="Register", 
                           command=register)
        submit.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        win.mainloop()

    def update_standings(self):
        self.table = tk.Text(self)
        self.table.insert(tk.END, tabulate(self.tnmt.table, headers='keys'))
        print(tabulate(self.tnmt.table, headers='keys'))
        self.table.place(x = 8, y = 8)       

if __name__ == '__main__':
    GUI().mainloop()
    