from spell_info import SpellInfo, example_spell
import json
import sqlite3

class SpellDataBase:
    def __init__(self, name: str):
        self.name = name

    def open_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.name)
        connection.execute('PRAGMA foreign_keys = ON')
        return connection

    def initialize_database(self, schema_filename: str):
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
        connection = self.open_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM {}".format(table))
        id_dict = {name: id_num for (id_num, name) in cursor.fetchall()}
        connection.close()
        return id_dict
    
    def add_spell(self, spell_info: SpellInfo):
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
        class_ids = self.get_ids('classes')
        used_ids = [class_ids[class_str] for class_str in class_list]
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
        school_ids = self.get_ids('schools')
        school = school_ids[spell_info.school]
        spell_dict = {
            'spell_name': spell_info.name,
            'spell_level': spell_info.level,
            'spell_school': school,
            'spell_ritual': int(spell_info.ritual),
            'spell_cast_time': spell_info.cast_time,
            'spell_range': spell_info.range,
            'spell_concentration': int(spell_info.concentration),
            'spell_duration': spell_info.duration,
            'spell_component_v': spell_info.components['V'],
            'spell_component_s': spell_info.components['S'],
            'spell_component_m': spell_info.components['M'],
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
    spell_db = SpellDataBase('test.sqlite3')
    spell_db.initialize_database('spell_db_schema.sql')
    spell_db.add_spell(example_spell)
    example_spell2 = example_spell
    example_spell2.name = 'Armor of Doofus'
    spell_db.add_spell(example_spell2)
    class_dict = spell_db.get_ids('classes')
    school_dict = spell_db.get_ids('schools')
    print(class_dict)
    print(school_dict)
    connection = spell_db.open_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM spells")
    print(cursor.fetchall())
    cursor.execute("SELECT * FROM spell_classes")
    print(cursor.fetchall())
    connection.close()
    pass