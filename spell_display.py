import tkinter as tk
import tkinter.ttk as ttk

window = tk.Tk()
window.columnconfigure(1, weight=1, minsize=75) # Sets the columns of the window grid to resize
window.rowconfigure(0, weight=1, minsize=75) # Sets the rows of the window grid to resize

spell_names = ["Poof", "Zap", "Alakazam", "Abracadabra", "Disintegrate", "Wish", "Fireball", "Speak with Animals", "Bless", "Augury", "Arms of Hadar", "Shillelagh", "Leomund's Tiny Hut", "Cure Wounds", "Mass Cure Wounds"]
spell_names = sorted(spell_names)

# Sets up the styles in the app
s = ttk.Style()
s.configure('SpellInfo.TLabel', background='beige')
s.configure('Emph.SpellInfo.TLabel', font='-size 10 -slant italic')
s.configure('SpellTitle.TLabel', background='beige', font='20')

# Converts Python list to the list type that tk uses
spell_namesvar = tk.StringVar(value=spell_names)

frm_spell_names = ttk.Frame(window, relief=tk.SUNKEN)
frm_spell_names.grid(column=0, row=0, padx=5, pady=5, sticky="nsew") # Positions this frame in the window grid
frm_spell_names.rowconfigure(0, weight=1) # Sets the row of the frame grid to resize

lstbx_spell_names = tk.Listbox(frm_spell_names, listvariable=spell_namesvar)
lstbx_spell_names.grid(column=0, row=0, sticky="nsew")

scrlbr_spell_names = ttk.Scrollbar(frm_spell_names, orient=tk.VERTICAL, command=lstbx_spell_names.yview)
scrlbr_spell_names.grid(column=1, row=0, sticky="ns")
lstbx_spell_names['yscrollcommand'] = scrlbr_spell_names.set # Connects the listbox back to the scrollbar to determine the visual motion of the bar

frm_spell_info = ttk.Frame(window, relief=tk.SUNKEN, style='SpellInfo.TLabel')
frm_spell_info.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")
frm_spell_info.columnconfigure([0,1], weight=1)

lbl_spell_name = ttk.Label(frm_spell_info, text="Spell Name", anchor=tk.CENTER, style='SpellTitle.TLabel')
lbl_spell_name.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

lbl_spell_ritual = ttk.Label(frm_spell_info, text="Ritual", anchor=tk.CENTER, style='Emph.SpellInfo.TLabel')
lbl_spell_ritual.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

lbl_spell_level = ttk.Label(frm_spell_info, text="Level 1", anchor=tk.CENTER, style='SpellInfo.TLabel')
lbl_spell_level.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

lbl_spell_school = ttk.Label(frm_spell_info, text="Abjuration", anchor=tk.CENTER, style='SpellInfo.TLabel')
lbl_spell_school.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

lbl_spell_cast_time = ttk.Label(frm_spell_info, text="Casting Time: 1 action", anchor=tk.CENTER, style='SpellInfo.TLabel')
lbl_spell_cast_time.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

lbl_spell_range = ttk.Label(frm_spell_info, text="Range: 60 ft", anchor=tk.CENTER, style='SpellInfo.TLabel')
lbl_spell_range.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

lbl_spell_duration = ttk.Label(frm_spell_info, text="Duration: Instantaneous", anchor=tk.CENTER, style='SpellInfo.TLabel')
lbl_spell_duration.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

lbl_spell_concentration = ttk.Label(frm_spell_info, text="Concentration", anchor=tk.CENTER, style='SpellInfo.TLabel')
lbl_spell_concentration.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

lbl_spell_components = ttk.Label(frm_spell_info, text="VSM*", anchor=tk.CENTER, style='SpellInfo.TLabel')
lbl_spell_components.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

txt_spell_components = tk.Text(frm_spell_info, width=50, height=2, borderwidth=0, background="beige", font='TkTextFont', wrap="word")
txt_spell_components.insert("1.0","Several small pieces of a broken bowl and a ruby worth at least 100 gp, which the spell consumes")
txt_spell_components.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky="nesw")

txt_spell_description = tk.Text(frm_spell_info, width=50, borderwidth=0, background="beige", font='TkTextFont', wrap="word")
txt_spell_description.insert("1.0","You throw a bowl full of porridge into the air. Each creature within 5 feet must make a Dexterity saving throw or be covered in porridge.\n\nThis spell does not affect gelatinous cubes.")
txt_spell_description['state'] = 'disabled'
txt_spell_description.grid(row=7, column=0, columnspan=2, padx=2, pady=2, sticky="nesw")



window.mainloop()