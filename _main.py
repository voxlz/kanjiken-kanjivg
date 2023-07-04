## An attempt to create a dependency tree including all JoYo kanji based on their parts.
from my_code.kanji import get_jinmeiyo_kanji, get_joyo_kanji
from my_code.kanjivg_utils import count_occurrences, expand_comps, find_similar, find_strokes, find_twins, get_comp_list_recursive, get_comp_list, simplify_comp_list, load_kanji, reduce_comps
from my_code.radicals import get_radicals, get_strokes
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
    comps = get_comp_list(kanji_obj)
    comps = reduce_comps(comps, char)
    comps = simplify_comp_list(comps)
    char_dict[char] = {
        'comps'  : comps,      # The components of the character
        'from'   : char,      # Character that this component is originally from
        'joyo'   : True,       # Whether this character is a joyo kanji
        'occur'  : 1,          # How often this char occurs as a comp, including itself
        'n_comps': len(comps),
        'derived': set(),        # Kanji this character occurs in
    }

# Add not-yet-encountered components to the dictionary, counting occurrences along the way. Has to be done AFTER all joyo kanji are added to the dictionary, to have the kanjivg data as a baseline.
for char in  joyo:
    kanji_obj = load_kanji(char)
    comps          = get_comp_list_recursive(kanji_obj)
    comps          = reduce_comps(comps, from_char=char)
    char_dict = count_occurrences(comps, char_dict, char)

for char in char_dict:
    find_strokes(char, char_dict)
    find_twins(char, char_dict)
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

for char in {'鑑', '猛', '漫', '環', '還', '価', '麓', '爵', '蔑', '益', '聴', '塩', '監', '皿'}:
    print(f"{char}: {char_dict[char]['comps']}")

# Print twin characters
seen = set()
for char in char_dict:
    if char in seen: continue
    twins = char_dict[char]['twins']
    seen |= twins
    if len(twins) > 0:
        print("Identical comp list: ", twins | {char}, char_dict[char]['comps'])

a = char_dict['為']

print()

# todo: make sure the new radicals drag-on and amongus are inserted in the right places.

# todo: not allow radicals of 3 strokes to be reduced. (or 4?) 土 工 should not be  ['十', '一'], unnecessary reduction.

# todo: for when svg is not found, check all it's homoglyphs as well.

# todo: huh:  㐅 ⼉ ['八'], ⼚ 丆 ['一', '㇒'], 由 田 ['⿙', '㇑', '二']

# todo: Low prio: ensure all strokes in kanjivg path element are actually in stroke list.

# Most repeated component in a kanji? 
# 傘 has 6 components: ['人', '人', '人', '人', '人', '十']

# Most strokes in a joyo kanji? 
# 鬱 has 29 strokes