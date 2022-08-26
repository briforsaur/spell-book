from dataclasses import dataclass
from itertools import compress

@dataclass
class SpellInfo:
    name: str
    level: int
    school: str
    ritual: bool
    cast_time: float
    range: str
    concentration: bool
    duration: str
    v_component: bool
    s_component: bool
    m_component: bool
    components: str
    components_tags: list
    description: str
    description_tags: list
    higher_levels: str
    higher_levels_tags: list
    in_class_spell_list: tuple[bool, bool, bool, bool, bool, bool, bool, bool]
    #
    levels = ('Cantrip', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th')
    schools = ('Abjuration', 'Conjuration', 'Divination', 'Enchantment', 'Evocation', 'Illusion', 'Necromancy', 'Transmutation')
    cast_time_units = ('reaction', 'bonus action', 'action', 'minutes', 'hours')
    cast_time_values = (0.01, 0.05, 0.1, 1, 60)
    range_units = ('Self', 'Touch', 'feet')
    classes = ('Bard', 'Cleric', 'Druid', 'Paladin', 'Ranger', 'Sorceror', 'Warlock', 'Wizard')

    def value_from_cast_time(time_quantity: int, time_unit: str) -> float:
        '''
        Converts a human-readable casting time to a numerical value.

        It is useful to represent casting times as numerical values
        for the purpose of sorting. For example, a reaction is 
        shorter than an action, 1 minute is shorter than 1 hour,
        etc. We can use minutes as the base unit because six-second
        rounds divide evenly into each 60-second minute. The 
        conversions for reactions and bonus actions are arbitrary
        but smaller than an action, which is taken to be the full
        six-second round even though a character can take multiple
        actions in many cases.

        The conversions are:

        1 reaction = 0.01

        1 bonus action = 0.05

        1 action = 0.1

        1 minute = 1 (and the standard conversion to hours)

        An example input to this function would be:

        value_from_cast_time(10, 'minutes')
        '''
        time_value = SpellInfo.cast_time_values[SpellInfo.cast_time_units.index(time_unit)]
        if time_unit == SpellInfo.cast_time_units[3] or time_unit == SpellInfo.cast_time_units[4]:
            time_value = time_quantity*time_value
        return time_value

    def get_cast_time_as_str(self) -> str:
        '''
        Converts a numerical value to a human-readable casting time.

        This function performs the inverse operation of the function
        value_from_cast_time. See that function for details.
        '''
        time_value = self.cast_time
        cast_time_str = 'None'
        if time_value < SpellInfo.cast_time_values[1]:
            # Reaction
            cast_time_str = '1 ' + SpellInfo.cast_time_units[0]
        elif time_value < SpellInfo.cast_time_values[2]:
            # Bonus action
            cast_time_str = '1 ' + SpellInfo.cast_time_units[1]
        elif time_value < SpellInfo.cast_time_values[3]:
            # Action
            cast_time_str = '1 ' + SpellInfo.cast_time_units[2]
        elif time_value < SpellInfo.cast_time_values[4]:
            # Minute
            cast_time_str = f'{int(time_value)} ' + SpellInfo.cast_time_units[3][:-1]
            if time_value > SpellInfo.cast_time_values[3]:
                # Plural minutes
                cast_time_str = cast_time_str + 's'
        else:
            # Hour
            cast_time_str = f'{int(time_value/60)} ' + SpellInfo.cast_time_units[4][:-1]
            if time_value > SpellInfo.cast_time_values[4]:
                # Plural hours
                cast_time_str = cast_time_str + 's'
        return cast_time_str

    def level_string_to_number(level_str: str) -> int:
        return SpellInfo.levels.index(level_str)

    def get_level_as_string(self) -> str:
        level_str = SpellInfo.levels[self.level]
        if self.level > 0:
            level_str = level_str + '-level'
        return level_str

    def get_vsm_components_as_string(self) -> str:
        vsm_str = ''
        if self.v_component:
            vsm_str += 'V'
        if self.s_component:
            vsm_str += 'S'
        if self.m_component:
            vsm_str += 'M'
        return vsm_str

    def get_classes_as_string(self) -> str:
        classes = compress(SpellInfo.classes, self.in_class_spell_list)
        return ", ".join(classes)

    def __str__(self) -> str:
        spell_info_str = ("{name}\n"
                          "{level} {school} {ritual}\n"
                          "Casting Time: {cast_time}\n"
                          "Range: {range}\n"
                          "Components: {vsm}{comp_details}\n"
                          "Duration: {concentration}{duration}\n"
                          "{description}\n"
                          "At Higher Levels: {higher_levels}\n"
                          "Classes: {classes}").format(
                                name=self.name,
                                level=self.get_level_as_string(),
                                school=self.school,
                                ritual='(ritual)' if self.ritual else '',
                                cast_time=self.get_cast_time_as_str(),
                                range=self.range,
                                vsm=self.get_vsm_components_as_string(),
                                comp_details= ' (' + self.components + ')' if self.components else '',
                                concentration='Concentration, up to ' if self.concentration else '',
                                duration=self.duration,
                                description=self.description,
                                higher_levels=self.higher_levels,
                                classes=self.get_classes_as_string())
        return spell_info_str


if __name__ == '__main__':
    spell_info = SpellInfo( name= 'Armor of Agathys',
                            level= 1,
                            school= 'Abjuration',
                            ritual= 0,
                            cast_time= SpellInfo.value_from_cast_time(1, 'action'),
                            range= 'Self',
                            v_component= True,
                            s_component= True,
                            m_component= True,
                            components= 'a cup of water', # If none, use an empty string
                            components_tags= [], # If none, use an empty list
                            concentration= 0,
                            duration= '1 hour',
                            description= 'A protective magical force surrounds you, manifesting as a spectral frost that covers you and your gear. You gain 5 temporary hit points for the duration. If a creature hits you with a melee attack while you have these hit points, the creature takes 5 cold damage.',
                            description_tags= [],
                            higher_levels= 'When you cast this spell using a spell slot of 2nd level or higher, both the temporary hit points and the cold damage increase by 5 for every level above 1st.',
                            higher_levels_tags= [],
                            in_class_spell_list=(False, False, False, False, False, False, True, False))
    print(spell_info)