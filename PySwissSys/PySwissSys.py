import tkinter as tk
import tkinter.filedialog
import tkinter.simpledialog
from pandastable import Table, TableModel
import td

class Standings(tk.Frame):
        def __init__(self, df, parent=None):
            self.parent = parent
            tk.Frame.__init__(self)
            self.main = self.master
            f = tk.Frame(self.main)
            f.pack(fill=tk.BOTH,expand=1)
            self.table = Table(f, dataframe=df, read_only=True, showstatusbar=True)
            self.table.show()
        
        def update(self, standings) -> None:
            self.table.updateModel(TableModel(standings))
            self.table.redraw()

class Pairings(tk.Toplevel):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        self.wm_title(f"Pairings for Round {master.tnmt.round}")
        self.setup_menu()
        self.chart = tk.Frame(master=self)
        self.chart.pack()
        self.table = Table(self.chart, dataframe=master.tnmt.pair(),
                           showstatusbar=True, showtoolbar=True)
        self.table.show()
    
    def setup_menu(self):
        self.menu = tk.Menu(self)
        result_menu = tk.Menu(self.menu, tearoff=0)
        result_menu.add_command(label="Finalize", command=self.update_results)
        self.menu.add_cascade(label='Results', menu=result_menu)
        self.config(menu=self.menu)
    
    def update_results(self, event=None):
        results = ([float(i) for i in self.table.model.df["WResult"].tolist()])
        self.master.tnmt.record_results(results)
        self.master.update_standings()
        self.destroy()

class ConfigGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("450x450")
        self.title("Welcome to PySwissSys")
        tk.Label(self, text="PySwissSys", font=("Bahnschrift", 24)).place(relx = 0.5, rely=0.25, anchor=tk.CENTER)
        
        new_tnmt = tk.Button(self, text="➕ New Tournament", font=("Bahnschrift", 14), command=self.new_tnmt)
        new_tnmt.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        open_tnmt = tk.Button(self, text="📁 Open an Existing Tournament", font=("Bahnschrift", 14), command=self.load_tnmt)
        open_tnmt.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
    
    def start(self, filename = None):
        self.destroy()
        TournamentGUI(self.tnmt, filename).mainloop()
    
    def load_tnmt(self):
        file = tkinter.filedialog.askopenfilename(title = "Select Tournament file",filetypes = (("Tournament Files","*.tnmt"),("All Files","*.*")))
        if file != "" and file.endswith("tnmt"):
            self.tnmt = td.Tournament.load(file)
            self.start(filename=file)
    
    def new_tnmt(self): 
        name = (tkinter.simpledialog.askstring("New Tournament", "Enter a name for the tournament: "))
        self.tnmt = td.Tournament(name = name)
        self.start()

class TournamentGUI(tk.Tk):
    def __init__(self, tnmt: td.Tournament, filename = None) -> None:
        super().__init__()
        self.geometry("800x450")
        self.tnmt = tnmt
        self.name = "Tournament: " + self.tnmt.title
        self.title(self.name)
        self.filename = filename
        self.standings = Standings(self.tnmt.table, parent=self)
        self.setup_menu()
        self.update_standings()
        self.bind('<F2>', self.add_player)
        self.bind('<F3>', self.pair)
        self.bind('<Control-q>', self.quit)
        self.bind('<Control-s>', self.save)

    def setup_menu(self):
        self.menu = tk.Menu(self)
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Save", command=self.save, accelerator="Ctrl+S")
        file_menu.add_command(label = "Exit", command=self.quit, accelerator="Ctrl+Q")
        reg_menu = tk.Menu(self.menu, tearoff=0)
        reg_menu.add_command(label = 'Register', command=self.add_player, accelerator="F2")
        reg_menu.add_command(label = "Register from CSV file", command=self.register_from_csv)
        pairing_menu = tk.Menu(self.menu, tearoff=0)
        pairing_menu.add_command(label="Pair next round...", command=self.pair, accelerator="F3")
        export_menu = tk.Menu(self.menu, tearoff=0)
        export_menu.add_command(label="Export all...", command=self.export)
        self.menu.add_cascade(label='File', menu=file_menu)
        self.menu.add_cascade(label='Players', menu = reg_menu)
        self.menu.add_cascade(label="Pairings", menu=pairing_menu)
        self.menu.add_cascade(label="Export", menu=export_menu)
        self.config(menu=self.menu)
    
    def add_player(self, event=None):
        def register(event=None):
            self.tnmt.add_player(td.Player(name.get(), float(uscf_rating.get()), uscf_id = uscf_id.get()))
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

        submit = tk.Button(win, text="Register", command=register)
        win.bind('<Return>',register)
        submit.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        win.mainloop()
    
    def register_from_csv(self, event=None):
        file = tkinter.filedialog.askopenfilename(title = "Select CSV",filetypes = (("Comma separated values","*.csv"),("All Files","*.*")))
        self.tnmt.register_from_csv(file)
        self.update_standings()

    def update_standings(self):
        self.tnmt.sort_players()
        self.standings.update(self.tnmt.table)
        self.show_as_unsaved()
    
    def save(self, event = None):
        if self.filename is None:
            self.filename = self.get_filename()
        self.tnmt.save(self.filename)
        self.title(self.name)
    
    def show_as_unsaved(self):
        self.title(self.name + "*")

    def get_filename(self) -> str:
        return tkinter.filedialog.asksaveasfilename(
            title = "Save as",
            filetypes = (("Tournament Files","*.tnmt"),("All Files","*.*")),
            initialfile = f"{self.tnmt.title}.tnmt"
        )

    def pair(self, event = None):
        Pairings(self).mainloop()
    
    def export(self, event=None):
        dir = tkinter.filedialog.askdirectory()
        print(dir)

    def quit(self, event=None):
        self.destroy()   

if __name__ == '__main__':
    ConfigGUI().mainloop()
    #TournamentGUI().mainloop()
    