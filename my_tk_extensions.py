from cgitb import text
import tkinter as tk
import tkinter.ttk as ttk
from typing import Dict, List, Tuple
from tkinter import font as tkFont

TagRange = tuple[str,str]
TagDict = dict[str,list[TagRange]]


class ExtendedTextBox(tk.Text):
    '''A text box with added useful methods.

    ExtendedTextBox is a subclass of the Tkinter Text widget. It adds 
    the following methods to make handling tags and text easier:

    extract_text_tags()

    apply_text_tags(tag_list)

    update_text_box(new_text, keep_tags)

    ExtendedTextBox also configures some tags to format text more 
    easily:

    'bold'

    'italic'

    'bolditalic'

    Each of the tags uses the default text box font.
    '''

    def __init__(self, parent, **keywords):
        '''
        Constructs new textboxes and configures tags

        See the superclass constructor for detailed documentation.

        The custom fonts and tags are defined on instantiation for each 
        text box object independently. This allows you to change the 
        font for each text box by manually editing the defined
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
    
    def extract_text_tags(self) -> TagDict:
        '''
        Extract all tags applied to this text box except the "sel" tag.

        The tags are returned as a dictionary of lists of tuples where 
        the keys of the dict are the tag name, and the values of the 
        dict are tuples of start and end indices of the text ranges 
        where the tag is applied.

        Example output:

        {
            'bold': [('1.0', '1.5'), ('2.0', 2.7')],
            'centering': [('1.0', '3.0')]
        }
        
        In the example, the 'bold' tag has been applied to two text 
        ranges, (1.0 to 1.5 and 2.0 to 2.7) while the 'centering' tag 
        has been applied to a single range.
        '''
        tag_names = list(self.tag_names())
        tag_names.remove('sel')
        saved_tags = {}
        for tag in tag_names:
            tag_ranges = self.tag_ranges(tag)
            grouped_tags = [
                (str(start_index), str(end_index)) for (start_index, end_index) 
                in zip(tag_ranges[::2],tag_ranges[1::2])]
            saved_tags.update({tag: grouped_tags})
        return saved_tags
    
    def apply_text_tags(self, tag_dict: TagDict):
        '''
        Apply a dictionary of tags to this text box.

        The tags in the dictionary are all applied to the text box for 
        the specified ranges. The tags must be configured to produce a 
        formatting effect.

        Example tag_list input:

        {
            'bold': [('1.0', '1.5'), ('2.0', 2.7')],
            'centering': [('1.0', '3.0')]
        }
        
        In the example, the 'bold' tag will be applied to two text 
        ranges, (1.0 to 1.5 and 2.0 to 2.7) while the 'centering' tag 
        will be applied to a single range.
        '''
        for tag in tag_dict.keys():
            tag_ranges = tag_dict[tag]
            for tag_range in tag_ranges:
                self.tag_add(tag, tag_range[0], tag_range[1])

    def update_text_box(self, new_text: str, keep_tags = False):
        '''
        Update a text box with entirely new text.

        Replaces the content of the text box with the string new_text.

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
        self.btn_boldtext = ttk.Button(
            self, text='Bold', 
            command= lambda: self.format_button_callback('bold')
        )
        self.btn_italictext = ttk.Button(
            self, text='Italic',
            command= lambda: self.format_button_callback('italic')
        )
        self.btn_bolditalictext = ttk.Button(
            self, text='Bold + Italic',
            command= lambda: self.format_button_callback('bolditalic')
        )
        self.btn_addbullet = ttk.Button(
            self, text='•', command=self.insert_bullet
        )
        self.txt_editor = ExtendedTextBox(
            self, width=100, height=10, borderwidth=1, font='TkTextFont',
            wrap="word")
        # Placing widgets on a grid
        self.btn_boldtext.grid(row=0, column=0, padx=[5, 2.5])
        self.btn_italictext.grid(row=0, column=1, padx=2.5)
        self.btn_bolditalictext.grid(row=0, column=2, padx=2.5)
        self.btn_addbullet.grid(row=0, column=3, padx=2.5)
        self.txt_editor.grid(
            row=1, column=0, columnspan=5, padx=5, pady=5, sticky='nsew'
        )

    def get(self):
        text_str = self.txt_editor.get('1.0', 'end')
        return text_str.strip()

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


def shift_tag_range(
        tag_range: TagRange, line_shift: int, char_shift: int) -> TagRange:
    """
    Shifts a pair of tag indices by a number of lines and characters

    This function is useful for combining formatted text sourced from 
    multiple text boxes. For example, when adding formatted text to a 
    text box that already has 4 lines of text, all the format tags of 
    the tags of the text being added would need to be shifted by 4 
    lines; or, when adding a prefix to some formatted text, such as
    "Name: ", the tags would need to be shifted by a set number of 
    characters (6 in the example given).

    Example input and output:
    tag_range = ('1.0', '1.12')
    line_shift = 4
    char_shift = 5

    output: ('5.5', '5.17')
    """
    shifted_tag_range = []
    for tag_index in tag_range:
        tag_index_numbers = [
            str(int(index_part) + shift)
            for (index_part, shift)
            in zip(tag_index.split('.'), (line_shift, char_shift))
        ]
        shifted_tag_range.append('.'.join(tag_index_numbers))
    return tuple(shifted_tag_range)


def shift_tag_dict(
        tag_dict: TagDict, line_shift: int, char_shift: int) -> TagDict:
    """
    Shifts an entire dictionary of tags by a number of lines and char.'s

    This function applies the shift_tag_range function to every tag 
    defined in a dictionary of tag ranges.

    Returns a new dictionary.
    """
    shifted_tag_dict = {}
    for tag in tag_dict.keys():
        shifted_range_list = [
                    shift_tag_range(tag_range, line_shift, char_shift)
                    for tag_range in tag_dict[tag]
                ]
        shifted_tag_dict.update({tag: shifted_range_list})
    return shifted_tag_dict


def add_tag_to_dict(tag_dict: TagDict, key: str, tag_range: TagRange):
    if key in tag_dict:
        tag_dict[key].append(tag_range)
    else:
        tag_dict.update({key: [tag_range,]})


def create_tagrange(start_line: int, start_char: int = 0, 
        end_line: int = None, end_char: int = None) -> TagRange:
    if end_line is None:
        end_line = start_line
    if end_char is None:
        end_char = 'end'
    start_index = '.'.join([str(start_line), str(start_char)])
    end_index = '.'.join([str(end_line), str(end_char)])
    tag_range = (start_index, end_index)
    return tag_range

if __name__ == "__main__":
    tag_storage = {}
    def save_tags(txt_editor: TextEditor):
        global tag_storage 
        tag_storage = txt_editor.txt_editor.extract_text_tags()
    def clear_tags(txt_editor: TextEditor):
        for tag in txt_editor.txt_editor.tag_names():
            txt_editor.txt_editor.tag_remove(tag, '1.0', 'end')
    def apply_tags():
        if tag_storage:
            txt_editor.txt_editor.apply_text_tags(tag_storage)
    def shift_tags(txt_editor: TextEditor, shift_list: list[int,int]):
        global tag_storage
        clear_tags(txt_editor)
        tag_storage = shift_tag_dict(tag_storage, *shift_list)
        apply_tags()

    root = tk.Tk()
    root.title('Tk Extensions')
    txt_editor = TextEditor(root)
    btn_save_tags = ttk.Button(
        root, text='Save Tags', command=lambda :save_tags(txt_editor)
    )
    btn_clear_tags = ttk.Button(
        root, text='Clear Tags', command=lambda :clear_tags(txt_editor)
    )
    btn_reapply_tags = ttk.Button(
        root, text='Reapply Tags', command=lambda :apply_tags()
    )
    btn_shift_tags_right = ttk.Button(
        root, text='Shift Tags Right', 
        command=lambda :shift_tags(txt_editor, [0, 1])
    )
    btn_shift_tags_down = ttk.Button(
        root, text='Shift Tags Down', 
        command=lambda :shift_tags(txt_editor, [1, 0])
    )
    txt_editor.pack(side="top", fill="both", expand=True)
    btn_save_tags.pack()
    btn_clear_tags.pack()
    btn_reapply_tags.pack()
    btn_shift_tags_right.pack()
    btn_shift_tags_down.pack()
    root.mainloop()