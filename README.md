# spell-book

## Description

This project aims to create a user-friendly interface for managing spells in Dungeons & Dragons 5th edition.
It allows a user to build their own database of spells and query that database with a simple GUI.
The user can filter the spells by a variety of properties.

The project is coded entirely in Python3 with a little bit of SQL.
The GUI is handled by Python's built-in tkinter library, so anyone with a Python installation should be able to run it.

Planned additions:
- add missing range units/specifiers (miles, sight)
- add persistent filter values in the filter window (and a "Reset to defaults" option)
- more filter options (components, costly components, casting time, range)
- sorting options (by name, level, casting time, range)
- search spells by name
- class archetype spell list options
- spell list/"loadout" builder
- database manager/open dialog

## Installation
This project cannot currently be "installed" in the traditional sense, but it should be easy to run.
The only prerequisite for this project is a Python3 installation.

1. Go to https://www.python.org/downloads/ and install Python. This project has been tested with 3.10.4, that version or later should work.
2. Download the latest release for this project.
3. Open a terminal and navigate to the project folder.
4. Run `python spell_display.py` in the terminal.

## User Guide

![The main app window](https://user-images.githubusercontent.com/66395421/226114190-06d909f6-6cda-491d-8579-a35d5db581d9.png)

When you run the app for the first time, you should be greeted with a window similar to the one above.
The app looks for a database named `phb_5e_spells.sqlite3`.
If that database file cannot be found, it initializes a new database.
Therefore, if you do not have a database already the spell list on the left side of the app will be blank.

You can create a new spell by clicking the "New Spell..." button on the bottom left.
Existing spells can be edited by selecting the spell from the list and clicking the "Edit Spell..." button.
Existing spells can also be deleted by selecting the spell from the list and clicking the "Delete Spell" button.
*WARNING: There is no confirmation dialog in the current version: if you click the "Delete Spell" button the spell is immediately and permanently deleted from the database.*

Selecting a spell from the list displays all the spell information in the pane on the right.
![The spell information display when a spell is selected from the list](https://user-images.githubusercontent.com/66395421/226115947-2884d1a1-f1aa-4525-bb5c-fb0d54b5a025.png)


### Creating New Spells/Editing Existing Spells
The New/Edit Spell dialog windows are the same, except when Edit Spell is selected, the window's fields will be pre-filled.

![image](https://user-images.githubusercontent.com/66395421/226114652-06b738f4-3412-4b33-bfe3-639ed7caa15d.png)
![image](https://user-images.githubusercontent.com/66395421/226114669-e3d77a46-7f8b-4124-8626-208fb0fdec8e.png)

Filling in the fields and clicking the "OK" button at the bottom of the window will add a new spell to the database (if New Spell... was selected) or edit an existing spell (if Edit Spell... was selected).
Clicking "Cancel" will discard all changes and return to the main window.

The following fields in this window are mandatory:
- Spell Name
- Level
- School
- Casting Time
- Range
- Duration

If those fields are not filled in you will probably get an error when you click "OK".
Tkinter recovers somewhat gracefully from those errors, the result will be that the window does not close and an error message will appear in the terminal.

#### Spell Name
The spell name can be typed into the Spell Name text field.

#### Level and School
The spell level and school can be selected from the corresponding dropdown fields.

#### Casting Time and Range
The Casting Time and Range fields are composed of two parts: a number box and a drop-down.
The number box is for giving a magnitude and the drop-down gives the unit.
You can use the scoll wheel in both boxes to quickly select different options.

In the Casting Time field the number box allows you to select any integer number greater than zero, and the drop-down allows you to select a unit.
The available units are: reaction, bonus action, action, minutes, and hours.
If you select reaction, bonus action, or action for the unit, the number box is ignored and the app assumes it to be 1.
Non-integer values can be entered manually but will result in an error.

The Range field number box allows you to enter an integer number greater than zero.
Scrolling in the number box will increment/decrement it in steps of 5.
The available units are: Self, Touch, feet.
When Self or Touch are selected, the number box is ignored and can be left blank.
Some spells have range units that are currently unsupported (miles, sight).
Miles can be represented in feet (just multiply by 5280 ft/mile).
Non-integer values can be entered manually but will result in an error.

#### Checkbox Fields
The checkbox fields (Ritual, Concentration, Components, and the Classes) have default values (unchecked for all boxes except the VSM components).
Checking the Ritual checkbox indicates that the spell can be cast as a ritual.
Checking the Concentration checkbox indicates that the spell requires concentration.
The components checkboxes indicate whether each type of spell component (V - verbal, S - somatic, M - material) are used in this spell.
Details on the material components can be added to the top textbox.

The class checkboxes are intended to show which classes have this spell on their spell list.
This only considers the default spellcaster class spell lists, not the additional spell options that many classes can gain from their class archetypes.

#### Text Boxes
The three large text boxes in the New/Edit spell window are for describing (from top to bottom) the spell material components, the description of the spell, and the "at higher levels" information for the spell.
Each text box supports basic text formatting by using the three buttons along the top of each text box.
The three format options (Bold, Italic, and Bold + Italic) are the only special formats used in the D&D 5e Player's Handbook spell descriptions.

Unlike a proper rich text editor, typing in bold, italic, or bold + italic is not supported.
Instead, after adding text to the text box, you can select the text and click one of the format buttons to add the corresponding formatting.
Selecting text that has already been formatted in this way and clicking the corresponding format button will delete the formatting.

You can also add bullets to the text by using the bullet button on the right side of the format buttons.
Bullets are also recognized if copied and pasted from other text.

Some spells in the Player's Handbook use tables to summarize more complicated spell descriptions.
Tables are not explicitly supported, but a table-like structure can be created in each text box by entering tabs.

The "At Higher Levels" textbox only requires the text that follows "At Higher Levels." in the spell description.
In the spell display window, the "At Higher Levels." text will be added automatically.

### Filtering Spells
Clicking the "Filter..." button at the top of the app will open a small dialog window.

![The filter dialog window in its default state.](https://user-images.githubusercontent.com/66395421/226117086-eb0e4b99-f221-4f47-b512-1b08b6d4553c.png)

By default the filter is set to select all spells.
Every time you re-open the filter window it will reset to the default values, allowing you to quickly turn off the filters.
Each drop-down allows you to filter the spell list by one of the spell properties.

The Ritual check-box allows you to find spells that can be cast as rituals.
When it is checked, only spells that can be cast as rituals will be displayed.
When it is not checked, spells with or without the Ritual property will be displayed.

Clicking the "Apply Filters" button will change the spell list in the main window to only show spells according to the values you selected.
Clicking "Cancel" will not make any change to the current filter state.
