## An attempt to create a dependency tree including all JoYo kanji based on their parts.
from typing import List
from my_code.kanji import get_jinmeiyo_kanji, get_joyo_kanji, get_valid_kanji
from my_code.kanjivg_utils import count_occurrences, get_comp_list_recursive, get_comp_list, load_kanji, reduce_comps_recursive
from my_code.radicals import get_radicals, get_strokes
from my_code.reduction import get_rules
from my_code.tree import Tree
from my_code.unicode import to_homoglyph

# Program limits
max_comps = 6 # how many kanji parts to allow in UI for a single kanji

# List of radicals to accept to reduce the number of components a kanji can have. Let's say... 8 components max.
radicals_8 = []

# Clear the cache of python 
import importlib
clear_cache = importlib.invalidate_caches()

def remove_duplicates(char_set, name):
    ''' Remove homoglyph duplicates from a set of
    characters with to_homoglyph. '''
    
    old_len = len(char_set)
    pref_chars = set(map(to_homoglyph, char_set))
    char_set = pref_chars.intersection(char_set)
    # removed = pref_chars.difference(char_set)
    print(f"{name}: {old_len} -> {len(char_set)} (-{old_len - len(char_set)})")
    return char_set

# Load all characters - Circular bullshit
joyo        = get_joyo_kanji()
strokes     = remove_duplicates(get_strokes(), 'strokes')
radicals    = remove_duplicates(get_radicals(), 'radicals')
jinmeiyo    = remove_duplicates(get_jinmeiyo_kanji(), 'jinmeiyo')

# Ensure no overlapping characters
assert radicals.isdisjoint(joyo)
assert joyo.isdisjoint(jinmeiyo)
assert radicals.isdisjoint(jinmeiyo)
    
def reduce_parts(strokes: List[str]):
    # '醸' = ['酉', '六', '一', '㇑*', '㇑*', '一', '一', '㇒*', '㇙*', '㇒*', '㇏*'] => ['酉', '六', '一', '㇑*', '㇑*', '二', '𧘇']
    strokes_str = ','.join(strokes)
    for (match, result) in get_rules():
        
        if match in strokes_str:
            # if match not in ['㇐*','㇑*']: 
            #     print(f"Reducing {strokes_str} to {result} in {kanji}")
            strokes_str = strokes_str.replace(match, result)
    
    # Split and remove empty strings
    return list(filter(lambda c: c, strokes_str.split(',')))

# Look up all joyo kanji in the kanji-svg database
char_dict = {} # All joyo kanji and their components 

# Create a base dictionary of all joyo kanji
for char in joyo:
    kanji_obj = load_kanji(char)
    comps = get_comp_list(kanji_obj)
    comps = reduce_parts(comps)
    char_dict[char] = {
        'comps'  : comps,      # The components of the character
        'from'   : char,      # Character that this component is originally from
        'joyo'   : True,       # Whether this character is a joyo kanji
        'occur'  : 1,          # How often this char occurs as a comp, including itself
        'n_comps': len(comps),
        'derived': set(),        # Kanji this character occurs in
    }

# Loop through all kanji and their components, adding not-yet-encountered components to the dictionary, counting occurrences along the way
for char in joyo:
    kanji_obj = load_kanji(char)
    comps     = get_comp_list_recursive(kanji_obj)
    comps     = reduce_comps_recursive(comps, from_char=char)
    char_dict = count_occurrences(comps, char_dict, char)

# How many have more than 'max_comps' components?
above_x_comps = [(char, info) for char, info in char_dict.items() if info['n_comps'] > max_comps]
print(f"More than {max_comps} components: {len(above_x_comps)}")
for (char, info) in above_x_comps:
    print(f"{char} has {info['n_comps']} components: {info['comps']}")

# given 'max_comps', how many radicals will the user encounter?
seen_strokes = set()
seen_radicals = set()
seen_other = set()
seen_name_kanji = set()
seen_components = len(char_dict)
for char in joyo:
    for part in char_dict[char]['comps']:
        if part not in joyo:
            if part in strokes: 
                seen_strokes.add(part)
            elif part in radicals:
                seen_radicals.add(part)
            elif part in jinmeiyo:
                seen_name_kanji.add(part)
            else:
                seen_other.add(part)

print(f"User will encounter {len(seen_strokes)} strokes")
print(seen_strokes)
print(f"User will encounter {len(seen_radicals)} radicals")
print(seen_radicals)
print(f"User will encounter {len(seen_name_kanji)} name kanji")
print(seen_name_kanji)
print(f"User will encounter {len(seen_other)} extra kanji")
print(seen_other)
print(f"User will encounter {seen_components} components")
print(len(joyo))

# I want consistency in my kanji components. The same kanji should always be represented by the same components. I cannot trust that kanjivg has done this for me, especially since I've edited some kanji, so I will have to do it myself. Therefore I require a dictionary of all kanji + radicals -> most reduced form. It should be based primarily on the corresponding kanjivg entry, and if not present in joyo but part of another kanji, then the most reduced form of that kanji should also be added.
a = char_dict['丶']
print()


# Most repeated component in a kanji? 
# 傘 has 6 components: ['人', '人', '人', '人', '人', '十']

# Most strokes in a joyo kanji? 
# 鬱 has 29 strokes