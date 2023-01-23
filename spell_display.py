from select import select
import tkinter as tk
import tkinter.ttk as ttk
from typing import Dict, List, Tuple
from tkinter import StringVar, font as tkFont

from my_tk_extensions import ExtendedTextBox, TextEditor, add_tag_to_dict, create_tagrange, shift_tag_dict
from spell_info import SpellInfo
from spelldb import SpellDataBase
from filter_window import SpellFilterWindow


class MainApplication(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.configure_layout()
        self.configure_styles()
        self.spell_list_pane = SpellListPane(self)
        self.spell_info_pane = SpellInfoPane(self)
        self.set_bindings()

        self.spell_list_pane.grid(
            column=0, row=0, padx=5, pady=5, sticky="nsew"
        )
        self.spell_info_pane.grid(
            column=1, row=0, padx=5, pady=5, sticky="nsew"
        )

    def configure_layout(self):
        # Setting the columns and rows to resize
        self.columnconfigure(1, weight=1, minsize=200)
        self.rowconfigure(0, weight=1, minsize=75)

    def configure_styles(self):
        self.style = ttk.Style()
        self.style.configure('SpellInfo.TFrame', background='beige')
        self.style.configure(
            'SpellTitle.TLabel', background='beige', font='20'
        )
        self.style.configure('SpellInfo.TLabel', background='beige')
        self.style.configure(
            'Emph.SpellInfo.TLabel', font='-size 10 -slant italic'
        )

    def set_bindings(self):
        self.spell_list_pane.bind(
            "<<SpellSelect>>", lambda e:self.spell_selection()
        )

    def spell_selection(self):
        spell_selected = self.spell_list_pane.get_list_selection()
        if spell_selected:
            spell_info = self.spell_list_pane.get_spell_info(spell_selected)
            self.spell_info_pane.update_spell_info(spell_info)


class SpellListPane(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, relief=tk.GROOVE, borderwidth=3)
        self.parent = parent
        self.spell_db = SpellDataBase('phb_5e_spells.sqlite3')
        self.filter = {'class_dict':{}, 'level':-1}
        self.get_spell_list()
        self.configure_layout()
        self.add_widgets()
        
    def configure_layout(self):
        self.rowconfigure(1, weight=1) # Row 0 can resize

    def add_widgets(self):
        # Converts Python list to the list type that tk uses
        self.spell_namesvar = tk.StringVar(value=list(self.spell_list.keys()))
        self.lstbx_spell_names = tk.Listbox(
            self, listvariable=self.spell_namesvar
        )
        self.scrlbr_spell_names = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.lstbx_spell_names.yview
        )
        # Connecting the listbox back to the scrollbar
        self.lstbx_spell_names['yscrollcommand'] = self.scrlbr_spell_names.set 
        # The SpellSelect event should be handled by the parent
        self.lstbx_spell_names.bind(
            "<<ListboxSelect>>",
            lambda e:self.event_generate('<<SpellSelect>>')
        )
        self.btn_new_spell = ttk.Button(
            self, text='New Spell...', command=self.new_spell_callback
        )
        self.btn_edit_spell = ttk.Button(
            self, text='Edit Spell...', command=self.edit_spell_callback
        )
        self.btn_del_spell = ttk.Button(
            self, text='Delete Spell', command=self.del_spell_callback
        )
        self.btn_filter = ttk.Button(
            self, text='Filter...', command=self.filter_callback
        )
        # Placing the widgets on the grid
        self.btn_filter.grid(column=3, row=0)
        self.lstbx_spell_names.grid(
            column=0, row=1, columnspan=4, sticky="nsew"
        )
        self.scrlbr_spell_names.grid(column=4, row=1, sticky="ns")
        self.btn_new_spell.grid(column=0, row=2)
        self.btn_edit_spell.grid(column=1, row=2)
        self.btn_del_spell.grid(column=2, row=2)

    def new_spell_callback(self):
        SpellEditWindow(self)

    def edit_spell_callback(self):
        spell_selected = self.get_list_selection()
        spell_info = self.get_spell_info(spell_selected)
        spell_id = self.spell_list[spell_info.name]
        SpellEditWindow(self, spell_info, spell_id)

    def del_spell_callback(self):
        spell_selected = self.get_list_selection()
        if spell_selected:
            spell_id = self.spell_list[spell_selected]
            self.spell_db.del_spell(spell_id)
            self.update_spell_listbox()

    def update_spell_listbox(self, select_spell: str=''):
        self.get_spell_list()
        self.spell_namesvar.set(list(self.spell_list.keys()))
        if select_spell:
            select_id = list(self.spell_list.keys()).index(select_spell)
        else:
            select_id = 0
        self.lstbx_spell_names.select_set(select_id)
        self.lstbx_spell_names.event_generate("<<ListboxSelect>>")

    def get_list_selection(self) -> str:
        selected_items = self.lstbx_spell_names.curselection()
        selected_spell = ''
        if selected_items:
            selected_spell = self.lstbx_spell_names.get(selected_items[0])
        return selected_spell

    def get_spell_info(self, spell_name: str) -> SpellInfo:
        spell_info = None
        if spell_name in self.spell_list.keys():
            spell_info = self.spell_db.get_spell(self.spell_list[spell_name])
        return spell_info

    def get_spell_list(self):
        self.spell_list = self.spell_db.query_spells(**self.filter)

    def update_spell_db(self, spell_info: SpellInfo, spell_id: int):
        # Can't have two spells with the same name
        if spell_info.name in self.spell_list.keys():
            # Checking to see if their IDs are the same (meaning a spell is
            # being updated)
            if spell_id != self.spell_list[spell_info.name]:
                i = 1
                spell_info.name = spell_info.name + str(i)
                while spell_info.name in self.spell_list.keys():
                    i += 1
                    spell_info.name = spell_info.name[0:-1] + str(i)
        if spell_id is not None:
            self.spell_db.update_spell(spell_id, spell_info)
        else:
            self.spell_db.add_spell(spell_info)
        self.update_spell_listbox(spell_info.name)
    
    def filter_callback(self):
        self.filter_window = SpellFilterWindow(self)
        self.filter_window.bind('<<ApplyFilter>>', self.filter_event_handler)

    def filter_event_handler(self, event: tk.Event):
        self.filter['class_dict'] = self.filter_window.frm_classes.get_chk_values()
        self.update_spell_listbox()



class SpellInfoPane(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(
            self, parent, relief=tk.GROOVE, borderwidth=3, 
            style='SpellInfo.TFrame'
        )
        self.parent = parent
        self.configure_layout()
        self.add_widgets()

    def configure_layout(self):
        # Two equal width, resizable columns
        self.columnconfigure([0,1], weight=1, minsize=200)
        self.rowconfigure(8, weight=1)

    def add_widgets(self):
        self.lbl_name = ttk.Label(
            self, anchor=tk.CENTER, style='SpellTitle.TLabel'
        )
        self.lbl_ritual = ttk.Label(
            self, anchor=tk.CENTER, style='Emph.SpellInfo.TLabel'
        )
        self.lbl_classes = ttk.Label(
            self, anchor=tk.CENTER, style='Emph.SpellInfo.TLabel'
        )
        self.lbl_level = ttk.Label(
            self, anchor=tk.CENTER, style='SpellInfo.TLabel'
        )
        self.lbl_school = ttk.Label(
            self, anchor=tk.CENTER, style='SpellInfo.TLabel'
        )
        self.lbl_cast_time = ttk.Label(
            self, anchor=tk.CENTER, style='SpellInfo.TLabel'
        )
        self.lbl_range = ttk.Label(
            self, anchor=tk.CENTER, style='SpellInfo.TLabel'
        )
        self.lbl_duration = ttk.Label(
            self, anchor=tk.CENTER, style='SpellInfo.TLabel'
        )
        self.lbl_concentration = ttk.Label(
            self, anchor=tk.CENTER, style='SpellInfo.TLabel'
        )
        self.lbl_components = ttk.Label(
            self, anchor=tk.CENTER, style='SpellInfo.TLabel'
        )
        self.txt_components = ExtendedTextBox(
            self, width=50, height=3, borderwidth=0, background="beige",
            font='TkTextFont', wrap="word"
        )
        self.frm_description = ttk.Frame(self, style='SpellInfo.TFrame')
        self.txt_description = ExtendedTextBox(
            self.frm_description, width=50, borderwidth=0, background="beige",
            font='TkTextFont', wrap="word"
        )
        self.scrlbr_description = ttk.Scrollbar(
            self.frm_description, orient=tk.VERTICAL, 
            command=self.txt_description.yview)
        self.txt_description['yscrollcommand'] = self.scrlbr_description.set
        self.txt_components['state'] = 'disabled'
        self.txt_description['state'] = 'disabled'
        # Placing the widgets on the grid
        self.lbl_name.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.lbl_classes.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.lbl_ritual.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.lbl_level.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.lbl_school.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.lbl_cast_time.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        self.lbl_range.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.lbl_duration.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        self.lbl_concentration.grid(
            row=5, column=1, padx=5, pady=5, sticky="ew"
        )
        self.lbl_components.grid(
            row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.txt_components.grid(
            row=7, column=0, columnspan=2, padx=5, pady=2, sticky="nesw"
        )
        self.frm_description.grid(
            row=8, column=0, columnspan=2, padx=5, pady=10, sticky="nesw"
        )
        self.txt_description.pack(
            side='left', expand=True, fill='both', padx=[0,5]
        )
        self.scrlbr_description.pack(side='right', fill='y')

    def update_spell_info(self, spell_info: SpellInfo):
        # Updating the labels
        self.lbl_name['text'] = spell_info.name
        self.lbl_ritual['text'] = 'Ritual' if spell_info.ritual else ''
        self.lbl_classes['text'] = spell_info.get_classes_as_string()
        self.lbl_level['text'] = spell_info.get_level_as_string()
        self.lbl_school['text'] = spell_info.school
        self.lbl_cast_time['text'] = ('Casting Time: ' 
            + spell_info.get_cast_time_as_str())
        self.lbl_range['text'] = 'Range: ' + spell_info.range
        self.lbl_duration['text'] = 'Duration: ' + spell_info.duration
        self.lbl_concentration['text'] = ('Concentration' 
            if spell_info.concentration else '')
        self.lbl_components['text'] = spell_info.get_vsm_components_as_string()
        # Updating the text boxes
        materials_text = spell_info.materials
        if materials_text:
            materials_text = '({})'.format(materials_text)
        self.txt_components.update_text_box(materials_text)
        # Shifting the materials text to account for the added parenthesis
        materials_tags_shifted = shift_tag_dict(
            spell_info.materials_tags, 0, 1
        )
        self.txt_components.apply_text_tags(materials_tags_shifted)
        self.txt_description.update_text_box(spell_info.description)
        self.txt_description['state'] = 'normal'
        self.txt_description.apply_text_tags(spell_info.description_tags)
        higher_levels_text = spell_info.higher_levels
        if higher_levels_text:
            higher_levels_prefix = '\n\nAt Higher Levels. '
            higher_levels_text = higher_levels_prefix + higher_levels_text
            higher_levels_line_offset = (
                spell_info.description + higher_levels_prefix
            ).count('\n')
            higher_levels_char_offset = len(higher_levels_prefix.strip('\n'))
            higher_levels_prefix_tags = create_tagrange(
                higher_levels_line_offset + 1, 
                end_char=higher_levels_char_offset
            )
            higher_levels_tags_shifted = shift_tag_dict(
                spell_info.higher_levels_tags, higher_levels_line_offset, 
                higher_levels_char_offset
            )
            add_tag_to_dict(
                higher_levels_tags_shifted, 'bolditalic', 
                higher_levels_prefix_tags
            )
            self.txt_description.insert('end', higher_levels_text)
            self.txt_description.apply_text_tags(higher_levels_tags_shifted)
        self.txt_description['state'] = 'disabled'


class SpellEditWindow(tk.Toplevel):
    def __init__(self, parent, spell_info: SpellInfo = None, 
            spell_id: int = None):
        super().__init__(parent)
        self.parent = parent
        self.spell_id = spell_id
        self.title('New Spell...')
        self.add_widgets()
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        if spell_info is not None:
            self.title('Edit Spell...')
            self.frm_spell_info.populate_fields(spell_info)
        # Defining close button behaviour
        self.protocol('WM_DELETE_WINDOW', self.dismiss) 
        # Making this the only interactable window
        self.wait_visibility()
        self.grab_set()

    def add_widgets(self):
        self.frm_spell_info = NewSpellPane(self)
        self.btn_confirm = ttk.Button(
            self, text='OK', command=self.confirm_close
        )
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
        self.parent.update_spell_db(
            self.frm_spell_info.get_spell_info(), self.spell_id)
        self.dismiss()


class NewSpellPane(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief=tk.GROOVE, borderwidth=3)
        self.parent = parent
        self.add_widgets()
        self.rowconfigure(list(range(0,12)), pad=5)
        # Allowing the text editors to stretch vertically
        self.rowconfigure(8, weight=2) 
        self.rowconfigure(10, weight=3)
        self.rowconfigure(12, weight=2)
        self.columnconfigure(6, weight=1)

    def add_widgets(self):
        self.lbl_name = ttk.Label(self, text="Spell Name")
        self.ent_name = ttk.Entry(self)
        self.lbl_level = ttk.Label(self, text="Level")
        self.cmb_level = ttk.Combobox(self)
        self.cmb_level['values'] = SpellInfo.levels
        self.cmb_level.state(["readonly"])
        self.lbl_school = ttk.Label(self, text="School")
        self.cmb_school = ttk.Combobox(self)
        self.cmb_school['values'] = SpellInfo.schools
        self.cmb_school.state(["readonly"])
        self.chk_ritual_value = tk.IntVar(value=False)
        self.chk_ritual = ttk.Checkbutton(self, text='Ritual', variable=self.chk_ritual_value, onvalue=True, offvalue=False)
        self.lbl_cast_time = ttk.Label(self, text="Casting Time")
        self.spn_cast_time = ttk.Spinbox(self, from_=1, to=60, increment=1)
        self.cmb_cast_unit = ttk.Combobox(self)
        self.cmb_cast_unit['values'] = SpellInfo.cast_time_units
        self.cmb_cast_unit.state(["readonly"])
        self.lbl_range = ttk.Label(self, text="Range")
        self.spn_range = ttk.Spinbox(self, from_=5, to=1000, increment=5)
        self.cmb_range_unit = ttk.Combobox(self)
        self.cmb_range_unit['values'] = SpellInfo.range_units
        self.cmb_range_unit.state(["readonly"])
        self.lbl_components = ttk.Label(self, text="Components")
        self.chk_components_V_value = tk.IntVar(value=True)
        self.chk_components_V = ttk.Checkbutton(self, text='V', variable=self.chk_components_V_value, onvalue=True, offvalue=False)
        self.chk_components_S_value = tk.IntVar(value=True)
        self.chk_components_S = ttk.Checkbutton(self, text='S', variable=self.chk_components_S_value, onvalue=True, offvalue=False)
        self.chk_components_M_value = tk.IntVar(value=True)
        self.chk_components_M = ttk.Checkbutton(self, text='M', variable=self.chk_components_M_value, onvalue=True, offvalue=False)
        self.txt_materials = TextEditor(self)
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
        self.txt_materials.grid(row=8, column=0, columnspan=7, sticky='nsew', padx=5)
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

    def get_spell_info(self):
        spell_info = SpellInfo(
            name=self.ent_name.get(),
            level=SpellInfo.level_string_to_number(self.cmb_level.get()),
            school=self.cmb_school.get(),
            ritual=self.chk_ritual_value.get(),
            cast_time=SpellInfo.value_from_cast_time(
                int(self.spn_cast_time.get()), self.cmb_cast_unit.get()
            ),
            range=SpellInfo.range_as_string(
                self.spn_range.get(), self.cmb_range_unit.get()
            ),
            concentration=self.chk_concentration_value.get(),
            duration=self.ent_duration.get(),
            components={
                'V': self.chk_components_V_value.get(),
                'S': self.chk_components_S_value.get(),
                'M': self.chk_components_M_value.get()
            },
            materials=self.txt_materials.get(),
            materials_tags=self.txt_materials.txt_editor.extract_text_tags(),
            description=self.txt_description.get(),
            description_tags=(
                self.txt_description.txt_editor.extract_text_tags()
            ),
            higher_levels=self.txt_higher_levels.get(),
            higher_levels_tags=(
                self.txt_higher_levels.txt_editor.extract_text_tags()
            ),
            in_class_spell_list={
                'Bard': self.chk_bard_value.get(),
                'Cleric': self.chk_cleric_value.get(),
                'Druid': self.chk_druid_value.get(),
                'Paladin': self.chk_paladin_value.get(),
                'Ranger': self.chk_ranger_value.get(),
                'Sorceror': self.chk_sorceror_value.get(),
                'Warlock': self.chk_warlock_value.get(),
                'Wizard': self.chk_wizard_value.get()
            }
        )
        return spell_info

    def populate_fields(self, spell_info: SpellInfo):
        self.ent_name.insert(0, spell_info.name)
        self.cmb_level.current(spell_info.level)
        self.cmb_school.current(spell_info.get_school_as_number())
        self.chk_ritual_value.set(spell_info.ritual)
        cast_time_tuple = spell_info.get_cast_time_as_quantity_and_unit()
        self.spn_cast_time.set(cast_time_tuple[0])
        self.cmb_cast_unit.current(
            SpellInfo.cast_time_units.index(cast_time_tuple[1])
        )
        range_tuple = spell_info.get_range_as_quantity_and_unit()
        self.spn_range.set(range_tuple[0])
        self.cmb_range_unit.current(
            SpellInfo.range_units.index(range_tuple[1])
        )
        self.chk_concentration_value.set(spell_info.concentration)
        self.ent_duration.insert(0, spell_info.duration)
        self.chk_components_V_value.set(spell_info.components['V'])
        self.chk_components_S_value.set(spell_info.components['S'])
        self.chk_components_M_value.set(spell_info.components['M'])
        self.txt_materials.txt_editor.update_text_box(
            spell_info.materials, allow_editing=True)
        self.txt_materials.txt_editor.apply_text_tags(
            spell_info.materials_tags
        )
        self.txt_description.txt_editor.update_text_box(
            spell_info.description, allow_editing=True)
        self.txt_description.txt_editor.apply_text_tags(
            spell_info.description_tags
        )
        self.txt_higher_levels.txt_editor.update_text_box(
            spell_info.higher_levels, allow_editing=True
        )
        self.txt_higher_levels.txt_editor.apply_text_tags(
            spell_info.higher_levels_tags
        )
        self.chk_bard_value.set(spell_info.in_class_spell_list['Bard'])
        self.chk_cleric_value.set(spell_info.in_class_spell_list['Cleric'])
        self.chk_druid_value.set(spell_info.in_class_spell_list['Druid'])
        self.chk_paladin_value.set(spell_info.in_class_spell_list['Paladin'])
        self.chk_ranger_value.set(spell_info.in_class_spell_list['Ranger'])
        self.chk_sorceror_value.set(spell_info.in_class_spell_list['Sorceror'])
        self.chk_warlock_value.set(spell_info.in_class_spell_list['Warlock'])
        self.chk_wizard_value.set(spell_info.in_class_spell_list['Wizard'])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("SpellBook")
    root.minsize(width=700, height=75)
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()