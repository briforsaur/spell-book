import tkinter as tk
import tkinter.ttk as ttk
from typing import Dict, List, Tuple
from tkinter import StringVar, font as tkFont

from my_tk_extensions import ExtendedTextBox, TextEditor
from spell_info import SpellInfo

spell_names = ["Poof", "Zap", "Alakazam", "Abracadabra", "Disintegrate", "Wish", "Fireball", "Speak with Animals", "Bless", "Augury", "Arms of Hadar", "Shillelagh", "Leomund's Tiny Hut", "Cure Wounds", "Mass Cure Wounds"]
spell_names = sorted(spell_names)

spell_data = SpellInfo( name= 'Bless',
                        ritual= 0,
                        level= 1,
                        school= 'Enchantment',
                        cast_time= SpellInfo.value_from_cast_time(1, 'action'),
                        duration= '1 minute',
                        range= '30 feet',
                        concentration= 1,
                        v_component= 1,
                        s_component= 1,
                        m_component= 1,
                        components= 'A sprinkling of holy water',
                        components_tags= [],
                        description= "You bless up to three creatures of your choice within range. Whenever a target makes an attack roll or a saving throw before the spell ends, the target can roll a d4 and add the number rolled to the attack roll or saving throw.",
                        description_tags= [('bold', '1.0', '1.5', '1.16', '1.24'), ('italic', '1.7', '1.14'), ('bolditalic', '3.0', '3.17')],
                        higher_levels= "When you cast a this spell using a spell slot of 2nd level or higher, you can target one additional creature for each slot level above 1st.",
                        higher_levels_tags= [],
                        in_class_spell_list=(False, True, False, False, False, False, False, False))

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
        win_new_spell = NewSpellWindow(self)

    def edit_spell_callback(self):
        pass

    def update_spell_entry(self, spell_info: Dict):
        print(spell_info)


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

    def update_spell_info(self, spell_info: SpellInfo):
        # Updating the labels
        self.lbl_name['text'] = spell_info.name
        self.lbl_ritual['text'] = 'Ritual' if spell_info.ritual else ''
        self.lbl_level['text'] = spell_info.get_level_as_string()
        self.lbl_school['text'] = spell_info.school
        self.lbl_cast_time['text'] = spell_info.get_cast_time_as_str()
        self.lbl_range['text'] = spell_info.range
        self.lbl_duration['text'] = spell_info.duration
        self.lbl_concentration['text'] = 'Concentration' if spell_info.concentration else ''
        self.lbl_components['text'] = spell_info.get_vsm_components_as_string()
        # Updating the text boxes
        self.txt_components.update_text_box(spell_info.components, keep_tags=True)
        self.txt_description.update_text_box(spell_info.description)
        self.txt_description['state'] = 'normal'
        self.txt_description.insert('end', '\n\nAt Higher Levels. ' + spell_info.higher_levels)
        self.txt_description.apply_text_tags(spell_info.description_tags)
        self.txt_description['state'] = 'disabled'


class NewSpellWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title('New Spell...')
        self.add_widgets()
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.protocol('WM_DELETE_WINDOW', self.dismiss) # Intercepting the close button
        # Making this the only interactable window
        self.wait_visibility()
        self.grab_set()

    def add_widgets(self):
        self.frm_spell_info = NewSpellPane(self)
        self.btn_confirm = ttk.Button(self, text='OK', command=self.confirm_close)
        self.btn_cancel = ttk.Button(self, text='Cancel', command=self.dismiss)
        # Placing the widgets on the grid
        self.frm_spell_info.grid(column=0, row=0, columnspan=3, sticky='nsew')
        self.btn_confirm.grid(column=0, row=1)
        self.btn_cancel.grid(column=1, row=1)

    def dismiss(self):
        # Returning interactivity to the other windows
        self.grab_release()
        self.destroy()

    def confirm_close(self):
        self.parent.update_spell_entry(self.frm_spell_info.get_spell_data())
        self.dismiss()


class NewSpellPane(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief=tk.GROOVE, borderwidth=3)
        self.parent = parent
        self.add_widgets()
        self.rowconfigure(list(range(0,12)), pad=5)
        self.rowconfigure(8, weight=2) # Allows the components text to stretch vertically
        self.rowconfigure(10, weight=3) # Allows the description text to stretch vertically
        self.rowconfigure(12, weight=2) # Allows the higher levels text to stretch vertically
        self.columnconfigure(6, weight=1)

    def add_widgets(self):
        self.lbl_name = ttk.Label(self, text="Spell Name")
        self.ent_name = ttk.Entry(self)
        self.lbl_level = ttk.Label(self, text="Level")
        self.cmb_level = ttk.Combobox(self)
        self.cmb_level['values'] = SpellInfo.levels
        self.lbl_school = ttk.Label(self, text="School")
        self.cmb_school = ttk.Combobox(self)
        self.cmb_school['values'] = SpellInfo.schools
        self.chk_ritual_value = tk.IntVar(value=False)
        self.chk_ritual = ttk.Checkbutton(self, text='Ritual', variable=self.chk_ritual_value, onvalue=True, offvalue=False)
        self.lbl_cast_time = ttk.Label(self, text="Casting Time")
        self.spn_cast_time = ttk.Spinbox(self, from_=1, to=60, increment=1)
        self.cmb_cast_unit = ttk.Combobox(self)
        self.cmb_cast_unit['values'] = SpellInfo.cast_time_units
        self.lbl_range = ttk.Label(self, text="Range")
        self.spn_range = ttk.Spinbox(self, from_=5, to=1000, increment=5)
        self.cmb_range_unit = ttk.Combobox(self)
        self.cmb_range_unit['values'] = SpellInfo.range_units
        self.lbl_components = ttk.Label(self, text="Components")
        self.chk_components_V_value = tk.IntVar(value=True)
        self.chk_components_V = ttk.Checkbutton(self, text='V', variable=self.chk_components_V_value, onvalue=True, offvalue=False)
        self.chk_components_S_value = tk.IntVar(value=True)
        self.chk_components_S = ttk.Checkbutton(self, text='S', variable=self.chk_components_S_value, onvalue=True, offvalue=False)
        self.chk_components_M_value = tk.IntVar(value=True)
        self.chk_components_M = ttk.Checkbutton(self, text='M', variable=self.chk_components_M_value, onvalue=True, offvalue=False)
        self.txt_components = TextEditor(self)
        self.lbl_duration = ttk.Label(self, text="Duration")
        self.ent_duration = ttk.Entry(self)
        self.chk_concentration_value = tk.IntVar(value=False)
        self.chk_concentration = ttk.Checkbutton(self, text='Concentration', variable=self.chk_concentration_value, onvalue=True, offvalue=False)
        self.frm_classes = ttk.Frame(self, relief='groove')
        self.chk_bard_value = tk.IntVar(value=False)
        self.chk_bard = ttk.Checkbutton(self.frm_classes, text='Bard', variable=self.chk_bard_value, onvalue=True, offvalue=False)
        self.chk_cleric_value = tk.IntVar(value=False)
        self.chk_cleric = ttk.Checkbutton(self.frm_classes, text='Cleric', variable=self.chk_cleric_value, onvalue=True, offvalue=False)
        self.chk_druid_value = tk.IntVar(value=False)
        self.chk_druid = ttk.Checkbutton(self.frm_classes, text='Druid', variable=self.chk_druid_value, onvalue=True, offvalue=False)
        self.chk_paladin_value = tk.IntVar(value=False)
        self.chk_paladin = ttk.Checkbutton(self.frm_classes, text='Paladin', variable=self.chk_paladin_value, onvalue=True, offvalue=False)
        self.chk_ranger_value = tk.IntVar(value=False)
        self.chk_ranger = ttk.Checkbutton(self.frm_classes, text='Ranger', variable=self.chk_ranger_value, onvalue=True, offvalue=False)
        self.chk_sorceror_value = tk.IntVar(value=False)
        self.chk_sorceror = ttk.Checkbutton(self.frm_classes, text='Sorceror', variable=self.chk_sorceror_value, onvalue=True, offvalue=False)
        self.chk_warlock_value = tk.IntVar(value=False)
        self.chk_warlock = ttk.Checkbutton(self.frm_classes, text='Warlock', variable=self.chk_warlock_value, onvalue=True, offvalue=False)
        self.chk_wizard_value = tk.IntVar(value=False)
        self.chk_wizard = ttk.Checkbutton(self.frm_classes, text='Wizard', variable=self.chk_wizard_value, onvalue=True, offvalue=False)
        self.lbl_description = ttk.Label(self, text='Description')
        self.txt_description = TextEditor(self)
        self.lbl_higher_levels = ttk.Label(self, text='At Higher Levels')
        self.txt_higher_levels = TextEditor(self)
        # Placing widgets on the grid
        self.lbl_name.grid(row=0, column=0, sticky='e')
        self.ent_name.grid(row=0, column=1, columnspan=4, sticky='ew')
        self.lbl_level.grid(row=1, column=0, sticky='e')
        self.cmb_level.grid(row=1, column=1, columnspan=3)
        self.chk_ritual.grid(row=1, column=4, sticky='w', padx=3)
        self.lbl_school.grid(row=2, column=0, sticky='e')
        self.cmb_school.grid(row=2, column=1, columnspan=3)
        self.lbl_cast_time.grid(row=4, column=0, sticky='e')
        self.spn_cast_time.grid(row=4, column=1, columnspan=3)
        self.cmb_cast_unit.grid(row=4, column=4, padx=[2,0])
        self.lbl_range.grid(row=5, column=0, sticky='e')
        self.spn_range.grid(row=5, column=1, columnspan=3)
        self.cmb_range_unit.grid(row=5, column=4, padx=[2,0])
        self.lbl_duration.grid(row=6, column=0, sticky='e')
        self.ent_duration.grid(row=6, column=1, columnspan=3, sticky='ew')
        self.chk_concentration.grid(row=6, column=4, sticky='w', padx=3)
        self.lbl_components.grid(row=7, column=0, sticky='e')
        self.chk_components_V.grid(row=7, column=1)
        self.chk_components_S.grid(row=7, column=2)
        self.chk_components_M.grid(row=7, column=3)
        self.txt_components.grid(row=8, column=0, columnspan=7, sticky='nsew', padx=5)
        self.frm_classes.grid(row=0, column=5, rowspan=6, padx=5)
        self.chk_bard.grid(row=0, column=0, padx=5, pady=2.5, sticky='w')
        self.chk_cleric.grid(row=1, column=0, padx=5, pady=2.5, sticky='w')
        self.chk_druid.grid(row=2, column=0, padx=5, pady=2.5, sticky='w')
        self.chk_paladin.grid(row=3, column=0, padx=5, pady=2.5, sticky='w')
        self.chk_ranger.grid(row=0, column=1, padx=5, pady=2.5, sticky='w')
        self.chk_sorceror.grid(row=1, column=1, padx=5, pady=2.5, sticky='w')
        self.chk_warlock.grid(row=2, column=1, padx=5, pady=2.5, sticky='w')
        self.chk_wizard.grid(row=3, column=1, padx=5, pady=2.5, sticky='w')
        self.lbl_description.grid(row=9, column=0, sticky='w')
        self.txt_description.grid(row=10, column=0, columnspan=7, sticky='nsew', padx=5)
        self.lbl_higher_levels.grid(row=11, column=0, sticky='w')
        self.txt_higher_levels.grid(row=12, column=0, columnspan=7, sticky='nsew', padx=5)

    def get_spell_data(self):
        spell_data = SpellInfo(
            name=self.ent_name.get(),
            level=SpellInfo.level_string_to_number(self.cmb_level.get()),
            school=self.cmb_school.get(),
            ritual=self.chk_ritual_value.get(),
            cast_time=SpellInfo.value_from_cast_time(int(self.spn_cast_time.get()), self.cmb_cast_unit.get()),
            range=SpellInfo.range_as_string(self.spn_range.get(), self.cmb_range_unit.get()),
            concentration=self.chk_concentration_value.get(),
            duration=self.ent_duration.get(),
            v_component=self.chk_components_V_value.get(),
            s_component=self.chk_components_S_value.get(),
            m_component=self.chk_components_M_value.get(),
            components=self.txt_components.get(),
            components_tags=self.txt_components.txt_editor.extract_text_tags(),
            description=self.txt_description.get(),
            description_tags=self.txt_description.txt_editor.extract_text_tags(),
            higher_levels=self.txt_higher_levels.get(),
            higher_levels_tags=self.txt_higher_levels.txt_editor.extract_text_tags(),
            in_class_spell_list=(
                self.chk_bard_value.get(),
                self.chk_cleric_value.get(),
                self.chk_druid_value.get(),
                self.chk_paladin_value.get(),
                self.chk_ranger_value.get(),
                self.chk_sorceror_value.get(),
                self.chk_warlock_value.get(),
                self.chk_wizard_value.get()
                )
            )
        return spell_data


if __name__ == "__main__":
    root = tk.Tk()
    root.title("SpellBook")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()