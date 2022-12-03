import tkinter as tk
import tkinter.ttk as ttk
from spell_info import SpellInfo


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
        self.frm_classes = CheckboxGroup(
            self, SpellInfo.classes, initial_class_chk_values, 2,
            relief=tk.GROOVE
        )
        # Placing the widgets on the grid
        self.frm_classes.grid(column=0, row=0, columnspan=2, padx=5, pady=5)
        self.btn_confirm.grid(column=4, row=5)
        self.btn_cancel.grid(column=5, row=5)

    def dismiss(self):
        # Returning interactivity to the other windows
        self.grab_release()
        self.destroy()

    def confirm_close(self):
        print(self.frm_classes.get_chk_values())
        self.dismiss()

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


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Filter Test")
    root.minsize(width=300, height=75)
    btn_open_window = ttk.Button(
        root, text="Filter...", command=lambda :SpellFilterWindow(root)
    )
    lbl_output = ttk.Label(root,text="---Output---")
    btn_open_window.pack()
    lbl_output.pack()
    root.mainloop()