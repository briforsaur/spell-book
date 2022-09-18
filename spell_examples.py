from spell_info import SpellInfo

spell1 = SpellInfo(
    name= 'Bless',
    ritual= 0,
    level= 1,
    school= 'Enchantment',
    cast_time= SpellInfo.value_from_cast_time(1, 'action'),
    duration= '1 minute',
    range= '30 feet',
    concentration= 1,
    components={'V': True, 'S': True, 'M': True},
    materials= 'a sprinkling of holy water',
    materials_tags= {},
    description= (
        "You bless up to three creatures of your choice within range. "
        "Whenever a target makes an attack roll or a saving throw before the "
        "spell ends, the target can roll a d4 and add the number rolled to "
        "the attack roll or saving throw."
    ),
    description_tags= {
        'bold': [('1.16', '1.24')], 'italic': [('1.7', '1.14')]
    },
    higher_levels= (
        "When you cast a this spell using a spell slot of 2nd level or higher,"
        " you can target one additional creature for each slot level above "
        "1st."
    ),
    higher_levels_tags= {'bold': [('1.49', '1.51')]},
    in_class_spell_list={
        'Bard': False, 'Cleric': True, 'Druid': False, 
        'Paladin': False, 'Ranger': False, 'Sorceror': False,
        'Warlock': False, 'Wizard': False
    }
)
spell2 = SpellInfo(
    name= 'False Life',
    ritual= 0,
    level= 1,
    school= 'Necromancy',
    cast_time= SpellInfo.value_from_cast_time(1, 'action'),
    duration= '1 hour',
    range= 'Self',
    concentration= 0,
    components={'V': True, 'S': True, 'M': True},
    materials= 'a small amount of alcohol or distilled spirits',
    materials_tags= {},
    description=(
        "Bolstering yourself with a necromantic facsimile of life, you gain "
        "1d4 + 4 temporary hit points for the duration."
    ),
    description_tags= {
        'bold': [('1.67', '1.74')]
    },
    higher_levels=(
        "When you cast a this spell using a spell slot of 2nd level or higher,"
        " you gain 5 additional temporary hit points for each slot level above"
        " 1st."
    ),
    higher_levels_tags= {},
    in_class_spell_list={
            'Bard': False, 'Cleric': True, 'Druid': False, 
            'Paladin': False, 'Ranger': False, 'Sorceror': True,
            'Warlock': False, 'Wizard': True
        }
)

spell3 = SpellInfo(
    name= 'Armor of Agathys',
    level= 1,
    school= 'Abjuration',
    ritual= 0,
    cast_time= SpellInfo.value_from_cast_time(1, 'action'),
    range= 'Self',
    components={'V': True, 'S': False, 'M': True},
    materials= 'a cup of water', # If none, use an empty string
    materials_tags= {}, # If none, use an empty dict
    concentration= 0,
    duration= '1 hour',
    description= ('A protective magical force surrounds you, manifesting '
        'as a spectral frost that covers you and your gear. You gain 5 '
        'temporary hit points for the duration. If a creature hits you '
        'with a melee attack while you have these hit points, the creature'
        ' takes 5 cold damage.'),
    description_tags= {'bold': [('1.114', '1.138'), ('1.0', '1.7')]},
    higher_levels= ('When you cast this spell using a spell slot of 2nd '
        'level or higher, both the temporary hit points and the cold '
        'damage increase by 5 for every level above 1st.'),
    higher_levels_tags= {},
    in_class_spell_list={
        'Bard': False, 'Cleric': False, 'Druid': False, 
        'Paladin': False, 'Ranger': False, 'Sorceror': False,
        'Warlock': True, 'Wizard': False
    }
)

spell_list = {
    spell1.name: spell1, 
    spell2.name: spell2,
    spell3.name: spell3
}