import tkinter as tk
import tkinter.ttk as ttk
from typing import Dict, List, Tuple
from tkinter import font as tkFont

class ExtendedTextBox(tk.Text):
    '''A text box with added useful methods.

    ExtendedTextBox is a subclass of the Tkinter Text widget. It adds the 
    following methods to make handling tags and text easier:

    extract_text_tags()

    apply_text_tags(tag_list)

    update_text_box(new_text, keep_tags)

    ExtendedTextBox also configures some tags to format text more easily:

    'bold'

    'italic'

    'bolditalic'

    Each of the tags uses the default text box font.
    '''

    def __init__(self, parent, **keywords):
        '''
        Constructs new textboxes and configures tags

        See the superclass constructor for detailed documentation.

        The custom fonts and tags are defined on instantiation for
        each text box object independently. This allows you to change
        the font for each text box by manually editing the defined
        fonts and reconfiguring the tags.
        '''
        tk.Text.__init__(self, parent, **keywords)
        self.parent = parent
        # Creating custom fonts
        default_font = tkFont.nametofont(self.cget("font"))
        bold_font = tkFont.Font(**default_font.configure())
        italic_font = tkFont.Font(**default_font.configure())
        bolditalic_font = tkFont.Font(**default_font.configure())
        bold_font.configure(weight="bold")
        italic_font.configure(slant="italic")
        bolditalic_font.configure(weight="bold", slant="italic")
        # Configuring custom text style tags
        self.tag_configure('bold',font=bold_font)
        self.tag_configure('italic',font=italic_font)
        self.tag_configure('bolditalic',font=bolditalic_font)
    
    def extract_text_tags(self) -> List[Tuple[str,...]]:
        '''
        Extract all tags applied to this text box except the "selection" tag.

        The tags are returned as a list of tuples where the first element 
        is a character string of the tag name, and the following elements 
        are pairs of start and end indices of the text ranges where the tag
        is applied.

        Example output:

        [('bold', '1.0', '1.5', '2.0', 2.7'),
        ('centering', '1.0', '3.0')]
        
        In the example, the 'bold' tag has been applied to two text ranges,
        (1.0 to 1.5 and 2.0 to 2.7) while the 'centering' tag has been 
        applied to a single range.
        '''
        tag_names = list(self.tag_names())
        tag_names.remove('sel')
        tag_ranges = [self.tag_ranges(tag) for tag in tag_names]
        saved_tags = [tuple([tag_name]) + tag_range for (tag_name, tag_range) in zip(tag_names, tag_ranges)]
        return saved_tags
    
    def apply_text_tags(self, tag_list: List[Tuple[str,...]]):
        '''
        Apply a list of tags to this text box.

        The tags in the list are all applied to the text box for the 
        specified ranges. The tags must be configured elsewhere to
        produce a formatting effect.

        Example tag_list input:

        [('bold', '1.0', '1.5', '2.0', 2.7'),
        ('centering', '1.0', '3.0')]
        
        In the example, the 'bold' tag will be applied to two text ranges,
        (1.0 to 1.5 and 2.0 to 2.7) while the 'centering' tag will be
        applied to a single range.
        '''
        for tag in tag_list:
            tag_name = tag[0]
            tag_ranges = tag[1:]
            for (start_index, end_index) in zip(tag_ranges[::2],tag_ranges[1::2]):
                self.tag_add(tag_name, start_index, end_index)

    def update_text_box(self, new_text: str, keep_tags = False):
        '''
        Update a text box with entirely new text.

        The content of the text box is replaced with the string new_text.

        The option keep_tags is useful for text boxes that should keep
        their formatting, such as centering, after updating.
        '''
        if keep_tags:
            saved_tags = self.extract_text_tags()
        self['state'] = 'normal'
        self.delete('1.0','end')
        self.insert('1.0',new_text)
        if keep_tags:
            self.apply_text_tags(saved_tags)
        self['state'] = 'disabled'


class TextEditor(ttk.Frame):
    def __init__(self, parent, **keywords):
        super().__init__(parent, **keywords)
        self.add_widgets()
        self.columnconfigure(4, weight=1)
        self.rowconfigure(1, weight=1)
        self.bold_text = False
        self.italic_text = False

    def add_widgets(self):
        self.btn_boldtext = ttk.Button(self, text='Bold', command= lambda: self.format_button_callback('bold'))
        self.btn_italictext = ttk.Button(self, text='Italic', command= lambda: self.format_button_callback('italic'))
        self.btn_bolditalictext = ttk.Button(self, text='Bold + Italic', command= lambda: self.format_button_callback('bolditalic'))
        self.btn_addbullet = ttk.Button(self, text='•', command=self.insert_bullet)
        self.txt_editor = ExtendedTextBox(self, width=100, height=10, borderwidth=1, font='TkTextFont', wrap="word")
        # Placing widgets on a grid
        self.btn_boldtext.grid(row=0, column=0, padx=[5, 2.5])
        self.btn_italictext.grid(row=0, column=1, padx=2.5)
        self.btn_bolditalictext.grid(row=0, column=2, padx=2.5)
        self.btn_addbullet.grid(row=0, column=3, padx=2.5)
        self.txt_editor.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='nsew')

    def get(self):
        return self.txt_editor.get('1.0', 'end')

    def format_button_callback(self, tag_name: str):
        selection_range = self.txt_editor.tag_ranges('sel')
        if selection_range:
            tags = self.txt_editor.tag_names(selection_range[0])
            if tag_name in tags:
                self.txt_editor.tag_remove(tag_name, *selection_range)
            else:
                self.txt_editor.tag_add(tag_name, *selection_range)
        self.txt_editor.focus_set() # returns focus to the text widgets

    def insert_bullet(self):
        self.txt_editor.insert('insert', ' • ')
        self.txt_editor.focus_set() # returns focus to the text widgets

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Tk Extensions')
    TextEditor(root).pack(side="top", fill="both", expand=True)
    root.mainloop()