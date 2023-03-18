from spell_info import SpellInfo, example_spell
import json
import sqlite3
from itertools import compress, chain

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

    def get_spell(self, spell_id: int) -> SpellInfo:
        connection = self.open_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM spells WHERE spell_id = ?", (spell_id,))
        # There is only 1 result in the cursor because spell_id is a prim. key
        result = cursor.fetchone()
        school_name = list(self.school_ids.keys())[
            list(self.school_ids.values()).index(result[3])
        ]
        spell_info = SpellInfo(
            name=result[1],
            level=result[2],
            school=school_name,
            ritual=bool(result[4]),
            cast_time=result[5],
            range=result[6],
            concentration=bool(result[7]),
            duration=result[8],
            components={'V':result[9], 'S':result[10], 'M':result[11]},
            materials=result[12],
            materials_tags=json.loads(result[13]),
            description=result[14],
            description_tags=json.loads(result[15]),
            higher_levels=result[16],
            higher_levels_tags=json.loads(result[17]),
            in_class_spell_list={}
        )
        cursor.execute(
            "SELECT class_id FROM spell_classes WHERE spell_id = ?", 
            (spell_id,)
        )
        result = cursor.fetchall()
        # result is a list of single-value tuples, which can be a simple list:
        result = [v[0] for v in result]
        class_membership = {k: v in result for (k, v) 
            in self.class_ids.items()
        }
        spell_info.in_class_spell_list.update(class_membership)
        return spell_info

    def get_spell_list(self) -> dict[str, int]:
        connection = self.open_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT spell_id, spell_name FROM spells ORDER BY spell_name ASC")
        spell_list = {name: spell_id for (spell_id, name) in cursor.fetchall()}
        connection.close()
        return spell_list

    def update_spell(self, spell_id: int, spell_info: SpellInfo):
        spell_dict = self.convert_spell_to_dict(spell_info)
        spell_dict['spell_id'] = spell_id
        connection = self.open_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE spells 
            SET
                spell_name = :spell_name,
                spell_level = :spell_level,
                spell_school = :spell_school,
                spell_ritual = :spell_ritual,
                spell_cast_time = :spell_cast_time,
                spell_range = :spell_range,
                spell_concentration = :spell_concentration,
                spell_duration = :spell_duration,
                spell_component_v = :spell_component_v,
                spell_component_s = :spell_component_s,
                spell_component_m = :spell_component_m,
                spell_materials = :spell_materials,
                spell_materials_tags = :spell_materials_tags,
                spell_description = :spell_description,
                spell_description_tags = :spell_description_tags,
                spell_higher_levels = :spell_higher_levels,
                spell_higher_levels_tags = :spell_higher_levels_tags
            WHERE spell_id = :spell_id
            """, spell_dict
        )
        connection.commit()
        connection.close()
        self.del_class_relations(spell_id)
        self.add_class_relations(spell_id, spell_info.get_classes_as_list())

    def del_class_relations(self, spell_id):
        connection = self.open_connection()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM spell_classes WHERE spell_id = ?", (spell_id,)
        )
        connection.commit()
        connection.close()

    def del_spell(self, spell_id: int):
        # Deletes class relations first to obey foreign key constraint
        self.del_class_relations(spell_id)
        connection = self.open_connection()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM spells WHERE spell_id = ?", (spell_id,)
        )
        connection.commit()
        connection.close()

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

    def query_spells(self, *, 
            class_dict: dict[str, bool]=None, 
            level: int=-1,
            school: str="",
            ritual: int=0) -> dict[str, int]:
        query_str = ("SELECT spells.spell_id, spells.spell_name\n"
            "FROM spells\n")
        join_statements = []
        query_statements = []
        parameters = []
        (class_join, class_query, classes) = self.build_class_query(class_dict)
        join_statements.append(class_join)
        if classes:
            query_statements.append(class_query)
            parameters.append(*classes)
        (level_query, level) = self.build_level_query(level)
        if level:
            query_statements.append(level_query)
            parameters.append(*level)
        (school_join, school_query, school) = self.build_school_query(school)
        join_statements.append(school_join)
        if school:
            query_statements.append(school_query)
            parameters.append(*school)
        if ritual:
            ritual_query = "spells.spell_ritual = ?"
            query_statements.append(ritual_query)
            parameters.append(ritual)
        # Appending all the statements to create the final query
        query_str += "".join(join_statements)
        if parameters:
            query_str += "WHERE "
            query_str += " AND ".join(query_statements) + "\n"
        query_str += "ORDER BY spells.spell_name ASC"
        print(query_str)
        connection = self.open_connection()
        cursor = connection.cursor()
        cursor.execute(query_str, tuple(parameters))
        spell_list = {name: spell_id for (spell_id, name) in cursor.fetchall()}
        connection.close()
        return spell_list
    
    def build_class_query(self, class_dict: dict[str, bool]
            ) -> tuple[str, str, tuple[str]]:
        join_str = ""
        query_str = ""
        classes = ()
        if (class_dict is not None 
                and any(class_dict.values()) and not all(class_dict.values())):
            classes = tuple(compress(class_dict.keys(), class_dict.values()))
            join_str = (
                "JOIN spell_classes ON spells.spell_id = "
                "spell_classes.spell_id\n"
                "JOIN classes ON spell_classes.class_id = classes.class_id\n"
            )
            query_str = "classes.class_name IN ({seq})".format(
                seq = ','.join(['?']*len(classes))
            )
        return (join_str, query_str, classes)

    def build_level_query(self, level: int) -> tuple[str, tuple[int]]:
        level_query = ""
        if level >= 0:
            level_query = "spells.spell_level = ?"
            level = (level,)
        else:
            level = ()
        return (level_query, level)

    def build_school_query(self, school: str) -> tuple[str, str, tuple[str]]:
        join_str = ""
        query_str = ""
        if school:
            join_str = (
                "JOIN schools ON spells.spell_school = schools.school_id\n"
            )
            query_str = "schools.school_name = ?"
            school = (school,)
        else:
            school = ()
        return (join_str, query_str, school)


if __name__ == '__main__':
    spell_db = SpellDataBase(
        'test.sqlite3', schema_filename='spell_db_schema.sql')
    spell_db.add_spell(example_spell)
    example_spell2 = example_spell
    example_spell2.name = 'Armor of Doofus'
    spell_db.add_spell(example_spell2)
    print(spell_db.class_ids)
    print(spell_db.school_ids)
    spell_list = spell_db.get_spell_list()
    print(spell_list)
    spell = spell_db.get_spell(spell_list['Armor of Agathys'])
    print(spell)
    example_spell2.in_class_spell_list.update({'Bard': True})
    example_spell2.name = 'Armor of Songs'
    example_spell2.higher_levels = ""
    example_spell2.higher_levels_tags = {}
    spell_db.update_spell(spell_list['Armor of Doofus'], example_spell2)
    spell_list = spell_db.get_spell_list()
    print(spell_list)
    spell = spell_db.get_spell(spell_list['Armor of Songs'])
    print(spell)
    spell_db.del_spell(spell_list['Armor of Songs'])
    print(spell_db.get_spell_list())