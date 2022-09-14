from spell_info import SpellInfo, example_spell
import json
import sqlite3

class SpellDataBase:
    '''
    Handles interactions with an sqlite3 database of spell information.

    This class is initialized with the name of an sqlite3 database and
    an optional schema filename if the user wishes to create a new 
    database or reset an old one.

    SpellDataBase expects a database containing the following tables 
    which should already exist or be defined in the optional schema:

    schools - A table to store the different spell schools.
        A two-column table where the first column, school_id, is the
        primary key and an alias of rowid, and the second column,
        school_name, contains the names of each spell school.

    classes - A table to store the different spellcasting classes.
        A two-column table where the first column, class_id, is the 
        primary key and an alias of rowid, and the second column,
        class_name, contains the names of each class.

    spells - A table that stores all the elements of a SpellInfo object.
        The first column is spell_id, the primary key and an alias of 
        rowid. The subsequent columns all use the same names as the 
        corresponding SpellInfo elements prefixed with "spell_" to avoid
        name clashes. For example, the SpellInfo element "name" becomes
        "spell_name". The only exceptions are the VSM components, which
        are each stored separately as "spell_component_v", etc. 

        The spell_school column is a foreign key column that references 
        the school_id from the schools table.

        All of the *_tags columns are stored as strings using Python's
        json dumps.

    spell_classes - An intersection table to link spells to classes.
        The table has two columns: spell_id, which is a foreign key 
        referencing the spell_id of the spells table, and class_id, 
        referencing the class_id of the classes table. This table allows
        a many-to-many relationship between the spells and the classes.
    '''
    def __init__(self, name: str, schema_filename = ''):
        self.name = name
        if schema_filename:
            self.initialize_database(schema_filename)
        self.class_ids = self.get_ids('classes')
        self.school_ids = self.get_ids('schools')

    def open_connection(self) -> sqlite3.Connection:
        '''
        Connects to the database with some configuration options set.

        This method enables foreign keys before returning a new sqlite3
        Connection object.
        
        The spell database uses foreign keys to enforce matching ID's 
        between the tables, specifically where tables use the class ID,
        school ID, or spell ID. According to the SQLite3 documentation,
        foreign keys must be enabled with every new connection to the 
        database.
        '''
        connection = sqlite3.connect(self.name)
        connection.execute('PRAGMA foreign_keys = ON')
        return connection

    def initialize_database(self, schema_filename: str):
        '''
        Creates or resets the tables in the database.

        This method creates new tables in the database according to a 
        schema file that contains an SQLite script. The schema is 
        expected to create four tables as described in the class 
        documentation.

        After creating the tables according to the schema file, this
        method populates the classes and schools tables according to the
        information supplied by the SpellInfo class. The IDs of each 
        school and class are not specified and allowed to be auto-
        generated by sqlite.
        '''
        connection = self.open_connection()
        cursor = connection.cursor()
        with open(schema_filename) as f:
            cursor.executescript(f.read())
        classes = [(name,) for name in SpellInfo.classes]
        cursor.executemany(
            "INSERT INTO classes (class_name) VALUES (?)", classes
        )
        schools = [(name,) for name in SpellInfo.schools]
        cursor.executemany(
            "INSERT INTO schools (school_name) VALUES (?)", schools
        )
        connection.commit()
        connection.close()

    def get_ids(self, table: str) -> dict[str, int]:
        '''
        Gets the IDs associated with the entries of a small table.

        The rowids of the classes and schools tables (class_id and
        school_id, respectively) are not assumed to be known or fixed,
        therefore this function serves to identify the mapping between
        the class and school names and their IDs in the database. This 
        mapping is needed to add entries to other tables which use
        these IDs as foreign keys.

        This method returns a dictionary where the keys are the names
        of each class or school and the values are the rowids. This 
        method will work for any two-column table where the first 
        column is the rowid and the second column is text.
        '''
        connection = self.open_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM {}".format(table))
        id_dict = {name: id_num for (id_num, name) in cursor.fetchall()}
        connection.close()
        return id_dict
    
    def add_spell(self, spell_info: SpellInfo):
        '''
        Adds a single spell to the database.

        This method adds a row to the spells table containing the
        information of the input SpellInfo object, then adds as many
        rows as needed to the spell_classes table to identify which
        classes can cast the spell.
        '''
        spell_dict = self.convert_spell_to_dict(spell_info)
        connection = self.open_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO spells (
                spell_name,
                spell_level,
                spell_school,
                spell_ritual,
                spell_cast_time,
                spell_range,
                spell_concentration,
                spell_duration,
                spell_component_v,
                spell_component_s,
                spell_component_m,
                spell_materials,
                spell_materials_tags,
                spell_description,
                spell_description_tags,
                spell_higher_levels,
                spell_higher_levels_tags
            )
            VALUES (
                :spell_name,
                :spell_level,
                :spell_school,
                :spell_ritual,
                :spell_cast_time,
                :spell_range,
                :spell_concentration,
                :spell_duration,
                :spell_component_v,
                :spell_component_s,
                :spell_component_m,
                :spell_materials,
                :spell_materials_tags,
                :spell_description,
                :spell_description_tags,
                :spell_higher_levels,
                :spell_higher_levels_tags
            )""", spell_dict
        )
        spell_id = cursor.lastrowid
        connection.commit()
        connection.close()
        self.add_class_relations(spell_id, spell_info.get_classes_as_list())

    def add_class_relations(self, spell_id: int, class_list: list[str]):
        '''
        Adds rows to the spell_classes table relating a spell to classes

        This method should not be used on its own, it is meant to be
        called by the add_spell method after it adds a new spell to 
        the database. It does not ensure that the spell_id is a valid
        foreign key before attempting to add it to the table.
        '''
        used_ids = [self.class_ids[class_str] for class_str in class_list]
        insertion_list = [(spell_id, class_id) for class_id in used_ids]
        connection = self.open_connection()
        cursor = connection.cursor()
        cursor.executemany(
            "INSERT INTO spell_classes VALUES (?,?)", insertion_list
        )
        connection.commit()
        connection.close()

    def get_spell(self, spell_name: str) -> SpellInfo:
        pass

    def convert_spell_to_dict(self, spell_info: SpellInfo) -> dict:
        '''
        Converts a SpellInfo object to a dictionary valid for entry.

        The output dictionary can be used with named placeholders in
        an SQL query string.

        The format expected by the database for spells differs from how
        they are stored in SpellInfo objects. For example, the school
        is stored as an integer in the database rather than a string,
        and the tags must be stored as strings using the json format.
        Also, booleans are stored as integers. While some of these 
        conversions could be performed implicitly by sqlite, this method
        explicitly converts each element to a type recognized by sqlite.
        '''
        school = self.school_ids[spell_info.school]
        spell_dict = {
            'spell_name': spell_info.name,
            'spell_level': spell_info.level,
            'spell_school': school,
            'spell_ritual': int(spell_info.ritual),
            'spell_cast_time': spell_info.cast_time,
            'spell_range': spell_info.range,
            'spell_concentration': int(spell_info.concentration),
            'spell_duration': spell_info.duration,
            'spell_component_v': int(spell_info.components['V']),
            'spell_component_s': int(spell_info.components['S']),
            'spell_component_m': int(spell_info.components['M']),
            'spell_materials': spell_info.materials,
            'spell_materials_tags': json.dumps(spell_info.materials_tags),
            'spell_description': spell_info.description,
            'spell_description_tags': json.dumps(spell_info.description_tags),
            'spell_higher_levels': spell_info.higher_levels,
            'spell_higher_levels_tags': json.dumps(
                spell_info.higher_levels_tags),
        }
        return spell_dict


if __name__ == '__main__':
    spell_db = SpellDataBase(
        'test.sqlite3', schema_filename='spell_db_schema.sql')
    spell_db.add_spell(example_spell)
    example_spell2 = example_spell
    example_spell2.name = 'Armor of Doofus'
    spell_db.add_spell(example_spell2)
    print(spell_db.class_ids)
    print(spell_db.school_ids)
    connection = spell_db.open_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM spells")
    print(cursor.fetchall())
    cursor.execute("SELECT * FROM spell_classes")
    print(cursor.fetchall())
    connection.close()
    pass