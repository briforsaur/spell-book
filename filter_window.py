import tkinter as tk
import tkinter.ttk as ttk
from spell_info import SpellInfo
from spelldb import SpellDataBase


class SpellFilterWindow(tk.Toplevel):
    def __init__(self, parent, **keywords) -> None:
        super().__init__(parent, **keywords)
        self.parent = parent
        self.title('Filter Spell List...')
        self.add_widgets()

    def add_widgets(self):
        self.btn_confirm = ttk.Button(
            self, text='Apply Filters', command=self.confirm_close
        )
        self.btn_cancel = ttk.Button(self, text='Cancel', command=self.dismiss)
        initial_class_chk_values = tuple(
            [True for x in range(len(SpellInfo.classes))]
        )
        self.frm_classes = ComboBoxGroup(
            self, label='Class', values=('Any', *SpellInfo.classes))
        self.frm_level = ComboBoxGroup(
            self, label='Level', values=('Any', *SpellInfo.levels))
        # self.frm_classes = CheckboxGroup(
        #     self, SpellInfo.classes, initial_class_chk_values, 2,
        #     relief=tk.GROOVE
        # )
        # Placing the widgets on the grid
        self.frm_classes.grid(column=0, row=0, columnspan=2, padx=5, pady=5)
        self.frm_level.grid(column=0, row=1, columnspan=2, padx=5, pady=5)
        self.btn_confirm.grid(column=4, row=5)
        self.btn_cancel.grid(column=5, row=5)

    def dismiss(self):
        # Returning interactivity to the other windows
        self.grab_release()
        self.destroy()

    def confirm_close(self):
        self.event_generate('<<ApplyFilter>>')
        self.dismiss()

    def get_filter_state(self) -> dict[str, str]:
        class_dict = {class_name: False for class_name in SpellInfo.classes}
        level = -1
        class_selection = self.frm_classes.get_value()
        level_str = self.frm_level.get_value()
        if class_selection != 'Any':
            class_dict[class_selection] = True
        if level_str != 'Any':
            level = SpellInfo.level_string_to_number(level_str)
        filter_state = {
            'Classes': class_dict,
            'Level': level
        }
        
        return filter_state


class CheckboxGroup(ttk.Frame):
    def __init__(self, parent, labels: tuple[str], initial_values: tuple[bool],
            num_columns: int, **keywords) -> None:
        super().__init__(parent, **keywords)
        self.parent = parent
        self.add_widgets(labels, initial_values, num_columns)

    def add_widgets(self, labels: tuple[str], initial_values: tuple[bool], 
            num_columns: int):
        self.chk_variables_dict = {}
        for id, label in enumerate(labels):
            label_key = label
            chk_value = tk.IntVar(value=initial_values[id])
            chk_class = ttk.Checkbutton(
                self, text=label, variable=chk_value
            )
            row_placement = id//num_columns
            col_placement = id%num_columns
            chk_class.grid(
                row=row_placement, column=col_placement, padx=5, pady=5
            )
            self.chk_variables_dict[label_key] = chk_value

    def get_chk_values(self) -> dict[str,bool]:
        chk_values = {key: self.chk_variables_dict[key].get()
            for key in self.chk_variables_dict
        }
        return chk_values

class ComboBoxGroup(ttk.Frame):
    def __init__(self, parent, label: str, values: tuple[str], **keywords):
        super().__init__(parent, **keywords)
        self.parent = parent
        self.lbl_label = ttk.Label(self, text=label)
        self.cmb_options = ttk.Combobox(self)
        self.cmb_options['values'] = values
        self.cmb_options.current(0)
        self.cmb_options.state(['readonly'])
        self.lbl_label.grid(column=0, row=0, padx=5)
        self.cmb_options.grid(column=1, row=0)

    def get_value(self) -> str:
        return self.cmb_options.get()


class _TestWindow(tk.Tk):
    def __init__(self, spell_db: str = '', **keywords):
        super().__init__(**keywords)
        self.spell_db = SpellDataBase(spell_db)
        self.btn_open_window = ttk.Button(
            self, text="Filter...", command=lambda :self.open_filter_window()
        )
        self.lbl_output = ttk.Label(self,text="---Output---")
        self.btn_open_window.pack()
        self.lbl_output.pack()

    def open_filter_window(self):
        self.filter_window = SpellFilterWindow(root)
        self.filter_window.bind('<<ApplyFilter>>', self.filter_event_handler)

    def filter_event_handler(self, event: tk.Event):
        filter_state = self.filter_window.get_filter_state()
        result = self.spell_db.query_spells(
            class_dict=filter_state['Classes'], 
            level=filter_state['Level']
        )
        print(result.keys())
        self.lbl_output['text'] = ', '.join(result.keys())

if __name__ == "__main__":
    root = _TestWindow(spell_db = 'phb_5e_spells.sqlite3')
    root.title("Filter Test")
    root.minsize(width=300, height=75)
    root.mainloop()