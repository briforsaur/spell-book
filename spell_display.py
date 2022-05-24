import tkinter as tk
import tkinter.ttk as ttk

spell_names = ["Poof", "Zap", "Alakazam", "Abracadabra", "Disintegrate", "Wish", "Fireball", "Speak with Animals", "Bless", "Augury", "Arms of Hadar", "Shillelagh", "Leomund's Tiny Hut", "Cure Wounds", "Mass Cure Wounds"]
spell_names = sorted(spell_names)


# Sets up the styles in the app
# s = ttk.Style()
# s.configure('SpellInfo.TLabel', background='beige')
# s.configure('Emph.SpellInfo.TLabel', font='-size 10 -slant italic')
# s.configure('SpellTitle.TLabel', background='beige', font='20')

class MainApplication(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.configure_layout()
        self.configure_styles()
        self.spell_list_pane = SpellListPane(self)
        self.spell_info_pane = SpellInfoPane(self)

        self.spell_list_pane.grid(column=0, row=0, padx=5, pady=5, sticky="nsew") # Positions this frame in the window grid
        self.spell_info_pane.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    def configure_layout(self):
        # Setting the columns and rows to resize
        self.columnconfigure(1, weight=1, minsize=75)
        self.rowconfigure(0, weight=1, minsize=75)

    def configure_styles(self):
        self.style = ttk.Style()
        self.style.configure('SpellInfo.TFrame', background='beige')
        self.style.configure('SpellTitle.TLabel', background='beige', font='20')
        self.style.configure('SpellInfo.TLabel', background='beige')
        self.style.configure('Emph.SpellInfo.TLabel', font='-size 10 -slant italic')


class SpellListPane(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, relief=tk.GROOVE, borderwidth=3)
        self.parent = parent
        self.configure_layout()
        self.add_widgets()
        
    def configure_layout(self):
        self.rowconfigure(0, weight=1) # Sets the row of the frame grid to resize

    def add_widgets(self):
        # Converts Python list to the list type that tk uses
        spell_namesvar = tk.StringVar(value=spell_names)
        self.lstbx_spell_names = tk.Listbox(self, listvariable=spell_namesvar)
        self.scrlbr_spell_names = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.lstbx_spell_names.yview)
        self.lstbx_spell_names['yscrollcommand'] = self.scrlbr_spell_names.set # Connects the listbox back to the scrollbar to determine the visual motion of the bar
        # Placing the widgets on the grid
        self.lstbx_spell_names.grid(column=0, row=0, sticky="nsew")
        self.scrlbr_spell_names.grid(column=1, row=0, sticky="ns")


class SpellInfoPane(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, relief=tk.GROOVE, borderwidth=3, style='SpellInfo.TFrame')
        self.parent = parent
        self.configure_layout()
        self.add_widgets()

    def configure_layout(self):
        # Two equal width, resizable columns
        self.columnconfigure([0,1], weight=1, minsize=200)

    def add_widgets(self):
        self.lbl_name = ttk.Label(self, text="Spell Name", anchor=tk.CENTER, style='SpellTitle.TLabel')
        self.lbl_ritual = ttk.Label(self, text="Ritual", anchor=tk.CENTER, style='Emph.SpellInfo.TLabel')
        self.lbl_level = ttk.Label(self, text="Level 1", anchor=tk.CENTER, style='SpellInfo.TLabel')
        self.lbl_school = ttk.Label(self, text="Abjuration", anchor=tk.CENTER, style='SpellInfo.TLabel')
        self.lbl_cast_time = ttk.Label(self, text="Casting Time: 1 action", anchor=tk.CENTER, style='SpellInfo.TLabel')
        self.lbl_range = ttk.Label(self, text="Range: 60 ft", anchor=tk.CENTER, style='SpellInfo.TLabel')
        self.lbl_duration = ttk.Label(self, text="Duration: Instantaneous", anchor=tk.CENTER, style='SpellInfo.TLabel')
        self.lbl_concentration = ttk.Label(self, text="Concentration", anchor=tk.CENTER, style='SpellInfo.TLabel')
        self.lbl_components = ttk.Label(self, text="VSM*", anchor=tk.CENTER, style='SpellInfo.TLabel')
        self.txt_components = tk.Text(self, width=50, height=2, borderwidth=0, background="beige", font='TkTextFont', wrap="word")
        self.txt_description = tk.Text(self, width=50, borderwidth=0, background="beige", font='TkTextFont', wrap="word")
        # Filling the text boxes with example text
        self.txt_components.insert("1.0","Several small pieces of a broken bowl and a ruby worth at least 100 gp, which the spell consumes")
        self.txt_description.insert("1.0","You throw a bowl full of porridge into the air. Each creature within 5 feet must make a Dexterity saving throw or be covered in porridge.\n\nThis spell does not affect gelatinous cubes.")
        self.txt_description['state'] = 'disabled'
        # Placing the widgets on the grid
        self.lbl_name.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.lbl_ritual.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.lbl_level.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.lbl_school.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.lbl_cast_time.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.lbl_range.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.lbl_duration.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        self.lbl_concentration.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.lbl_components.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.txt_components.grid(row=6, column=0, columnspan=2, padx=5, pady=2, sticky="nesw")
        self.txt_description.grid(row=7, column=0, columnspan=2, padx=5, pady=10, sticky="nesw")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("SpellBook")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()