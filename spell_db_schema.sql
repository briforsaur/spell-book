BEGIN;
DROP TABLE IF EXISTS spell_classes;
DROP TABLE IF EXISTS spells;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS schools;

PRAGMA foreign_keys = ON;

CREATE TABLE classes (class_id INTEGER PRIMARY KEY, class_name TEXT);

CREATE TABLE schools (school_id INTEGER PRIMARY KEY, school_name TEXT);

CREATE TABLE spells (
    spell_id INTEGER PRIMARY KEY,
    spell_name TEXT,
    spell_level INTEGER,
    spell_school INTEGER NOT NULL,
    spell_ritual INTEGER,
    spell_cast_time REAL,
    spell_range TEXT,
    spell_concentration INTEGER,
    spell_duration TEXT,
    spell_component_v INTEGER,
    spell_component_s INTEGER,
    spell_component_m INTEGER,
    spell_materials TEXT,
    spell_materials_tags TEXT,
    spell_description TEXT,
    spell_description_tags TEXT,
    spell_higher_levels TEXT,
    spell_higher_levels_tags TEXT,
    FOREIGN KEY (spell_school) REFERENCES schools(school_id)
);

CREATE TABLE spell_classes (
    spell_id INTEGER,
    class_id INTEGER,
    FOREIGN KEY (spell_id) REFERENCES spells(spell_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

COMMIT;