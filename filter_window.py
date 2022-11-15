import tkinter as tk
import tkinter.ttk as ttk


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
        # Placing the widgets on the grid
        self.btn_confirm.grid(column=0, row=1)
        self.btn_cancel.grid(column=1, row=1)

    def dismiss(self):
        # Returning interactivity to the other windows
        self.grab_release()
        self.destroy()

    def confirm_close(self):
        self.dismiss()


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