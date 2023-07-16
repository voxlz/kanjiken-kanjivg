## An attempt to create a dependency tree including all JoYo kanji based on their parts.
from collections import defaultdict
import csv
from matplotlib import pyplot
from src import trim_components
from src.kanji import get_jinmeiyo_kanji, get_joyo_kanji
from src.kanjivg_utils import count_occurrences, find_similar, set_strokes_parents_depth, find_twins, get_comp_list_recursive, simplify_comp_list, load_kanji, reduce_comps
from src.meanings import set_char_meanings
from src.order import set_learn_order
from src.radicals import get_radicals, get_strokes
from src.unicode import to_homoglyph


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
joyo             = get_joyo_kanji()
strokes      = remove_duplicates(get_strokes(), 'strokes')
radicals    = remove_duplicates(get_radicals(), 'radicals')
jinmeiyo    = remove_duplicates(get_jinmeiyo_kanji(), 'jinmeiyo')

# Ensure no overlapping characters
assert radicals.isdisjoint(joyo)
assert joyo.isdisjoint(jinmeiyo)
assert radicals.isdisjoint(jinmeiyo)

# Look up all joyo kanji in the kanji-svg database
char_dict = {} # All joyo kanji and their components 

# Create a base dictionary of all joyo kanji
for char in joyo:
    kanji_obj = load_kanji(char)
    comps = get_comp_list_recursive(kanji_obj)
    comps = reduce_comps(comps, char)
    comps = simplify_comp_list(comps)
    char_dict[char] = {
        'comps'  : comps,      # The components of the character
        'from'   : char,      # Character that this component is originally from
        'joyo'   : True,       # Whether this character is a joyo kanji
        'stroke'   : False,       # Whether this character is a joyo kanji
        'occur'  : 1,          # How often this char occurs as a comp, including itself
        'n_comps': len(comps),
        'derived': set(),        # Kanji this character occurs in
        'parent': set(),   # Kanji this character occurs in directly
    }

# Add not-yet-encountered components to the dictionary, counting occurrences along the way. Has to be done AFTER all joyo kanji are added to the dictionary, to have the kanjivg data as a baseline.
for char in  joyo:
    kanji_obj = load_kanji(char)
    comps          = get_comp_list_recursive(kanji_obj)
    comps          = reduce_comps(comps, from_char=char)
    char_dict = count_occurrences(comps, char_dict, char)


# -------------- CHAR DICT CREATED FOR ALL CHARACTERS -------------- #

# TODO: Radical Reduction
# trim_components(char_dict)

# Add meanings to all characters
set_char_meanings(char_dict)

# Calculate learn order
set_learn_order(char_dict)

for char in char_dict:
    set_strokes_parents_depth(char, char_dict)


a = list(char_dict.items())
a = list(sorted(a, key=lambda x:  len(x[1]['parent']), reverse=True))
most_used_non_stroke = list(filter(lambda x: not x[1]['stroke'], a))

if export := False: 
    for char in char_dict:
        find_twins(char, char_dict)

    for char in char_dict:
        find_similar(char, char_dict)

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

# Print twin characters
seen = set()
for char in char_dict:
    if char in seen: continue
    if "twins" not in char_dict[char]: break

    twins = char_dict[char]['twins']
    seen |= twins
    if len(twins) > 0:
        print("Identical comp list: ", twins | {char}, char_dict[char]['comps'])

depth = defaultdict(list)
comps =  defaultdict(list)

for char in char_dict:
    depth[char_dict[char]['depth']].append(char)
    comps[len(char_dict[char]['comps'])].append(char)

assert len(comps[0]) == len(seen_strokes), "All strokes should be in comps[0]"

x = list(depth.keys())
y = list(map(lambda x: len(x), depth.values()))
pyplot.figure("Depth")
pyplot.bar(x, y)
x = list(comps.keys())
y = list(map(lambda x: len(x), comps.values()))
pyplot.figure("Components")
pyplot.bar(x, y)
pyplot.show()




print()

for char in char_dict:
    assert char not in char_dict[char]['comps'], f"Character {char} is in its own components"

# todo: for when svg is not found, check all it's homoglyphs as well.

# todo: Low prio: ensure all strokes in kanjivg path element are actually in stroke list.

# Most repeated component in a kanji? 
# 傘 has 6 components: ['人', '人', '人', '人', '人', '十']

# Most strokes in a joyo kanji? 
# 鬱 has 29 strokes