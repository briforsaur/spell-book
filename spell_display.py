import tkinter as tk
import tkinter.ttk as ttk
from typing import Dict, List, Tuple
from tkinter import font as tkFont

from my_tk_extensions import ExtendedTextBox

spell_names = ["Poof", "Zap", "Alakazam", "Abracadabra", "Disintegrate", "Wish", "Fireball", "Speak with Animals", "Bless", "Augury", "Arms of Hadar", "Shillelagh", "Leomund's Tiny Hut", "Cure Wounds", "Mass Cure Wounds"]
spell_names = sorted(spell_names)

spell_data = {  'name': 'Bless',
                'ritual': False,
                'level': 1,
                'school': 'Enchantment',
                'cast-time': '1 action',
                'duration': '1 minute',
                'range': '30 feet',
                'concentration': True,
                'components': 'VSM',
                'component-text': 'A sprinkling of holy water',
                'description': "You bless up to three creatures of your choice within range. Whenever a target makes an attack roll or a saving throw before the spell ends, the target can roll a d4 and add the number rolled to the attack roll or saving throw.",
                'description-tags': [('bold', '1.0', '1.5', '1.16', '1.24'), ('italic', '1.7', '1.14'), ('bolditalic', '3.0', '3.17')],
                'higher-levels': "When you cast a this spell using a spell slot of 2nd level or higher, you can target one additional creature for each slot level above 1st."}

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
        self.btn_new_spell = ttk.Button(self, text='New Spell...', command=self.new_spell_callback)
        self.btn_edit_spell = ttk.Button(self, text='Edit Spell...', command=self.edit_spell_callback)
        # Placing the widgets on the grid
        self.lstbx_spell_names.grid(column=0, row=0, columnspan=3, sticky="nsew")
        self.scrlbr_spell_names.grid(column=3, row=0, sticky="ns")
        self.btn_new_spell.grid(column=0, row=1)
        self.btn_edit_spell.grid(column=1, row=1)

    def new_spell_callback(self):
        win_new_spell = tk.Toplevel(self)
        win_new_spell.title('New Spell...')

    def edit_spell_callback(self):
        pass


class SpellInfoPane(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, relief=tk.GROOVE, borderwidth=3, style='SpellInfo.TFrame')
        self.parent = parent
        self.configure_layout()
        self.add_widgets()
        self.update_spell_info(spell_data)

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
        self.txt_components = ExtendedTextBox(self, width=50, height=2, borderwidth=0, background="beige", font='TkTextFont', wrap="word")
        self.txt_description = ExtendedTextBox(self, width=50, borderwidth=0, background="beige", font='TkTextFont', wrap="word")
        # Filling the text boxes with example text
        self.txt_components.insert("1.0","Several small pieces of a broken bowl and a ruby worth at least 100 gp, which the spell consumes")
        self.txt_components.tag_add('centering', '1.0', 'end')
        self.txt_components.tag_configure('centering', justify=tk.CENTER)
        self.txt_components['state'] = 'disabled'
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

    def update_spell_info(self, spell_info: Dict):
        # Updating the labels
        self.lbl_name['text'] = spell_info['name']
        self.lbl_ritual['text'] = 'Ritual' if spell_info['ritual'] else ''
        self.lbl_level['text'] = f"{make_ordinal(spell_info['level'])}-level"
        self.lbl_school['text'] = spell_info['school']
        self.lbl_cast_time['text'] = spell_info['cast-time']
        self.lbl_range['text'] = spell_info['range']
        self.lbl_duration['text'] = spell_info['duration']
        self.lbl_concentration['text'] = 'Concentration' if spell_info['concentration'] else ''
        self.lbl_components['text'] = spell_info['components']
        # Updating the text boxes
        self.txt_components.update_text_box(spell_info['component-text'], keep_tags=True)
        self.txt_description.update_text_box(spell_info['description'])
        self.txt_description['state'] = 'normal'
        self.txt_description.insert('end', '\n\nAt Higher Levels. ' + spell_info['higher-levels'])
        self.txt_description.apply_text_tags(spell_info['description-tags'])
        self.txt_description['state'] = 'disabled'





def make_ordinal(n):
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'

    by Florian Brucker (https://stackoverflow.com/a/50992575)
    can be reused under the CC BY-SA 4.0 license (https://creativecommons.org/licenses/by-sa/4.0/)
    '''
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

if __name__ == "__main__":
    root = tk.Tk()
    root.title("SpellBook")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()