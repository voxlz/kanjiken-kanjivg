## An attempt to create a dependency tree including all JoYo kanji based on their parts.
import csv
from typing import List
from kanjivg import Stroke, isKanji, realord
from my_code.kanji import get_jinmeiyo_kanji, get_joyo_kanji
from my_code.unicode import to_homoglyph

from utils import canonicalId, listSvgFiles

# Program limits
max_comps = 6 # how many kanji parts to allow in UI for a single kanji

# List of radicals to accept to reduce the number of components a kanji can have. Let's say... 8 components max.
radicals_8 = []

# Clear the cache of python 
import importlib
clear_cache = importlib.invalidate_caches()

# Load all radicals
def hex_to_unicode_str(hex_str):
    return hex_str.replace("0x", "\\u").encode('utf-8').decode('unicode-escape')

radical_kanji_mapping = {}
with open("my_files/kanji_radical_mapping.csv", "r", encoding="utf8") as mapping:
    tsv_reader = csv.reader(mapping, delimiter=",")

    # Skip the first row, which is just the source link
    next(tsv_reader)

    for row in tsv_reader:
        (kanji, radical, *a) = row
        radical_kanji_mapping[hex_to_unicode_str(radical)] = hex_to_unicode_str(kanji)

kangxi_radicals = set()
with open("my_files/radicals_kangxi.tsv", "r", encoding="utf8") as radical_file:
    tsv_reader = csv.reader(radical_file, delimiter="\t")

    # Skip the first row, which is just the source link
    next(tsv_reader)

    for row in tsv_reader:
        radical = row[0]
        kangxi_radicals.add(to_homoglyph(radical))

# han_radicals = []
# for radical in kangxi_radicals:
#     s = unicodedata.decomposition(radical) # Not all radicals have a decomposition
#     s = s.replace("<compat> ", "\\u").encode('utf-8').decode('unicode-escape')
#     if s == "" and radical in radical_kanji_mapping:
#         s = radical_kanji_mapping[radical]
#     if s != "":
#         han_radicals.append(s)

radicals = kangxi_radicals # + han_radicals

joyo_kanji = get_joyo_kanji()
jinmeiyo_kanji = get_jinmeiyo_kanji()
valid_kanji = joyo_kanji.union(jinmeiyo_kanji)
# This one is not in the joyo kanji list, but is used in the kanji-svg database
valid_kanji.add('并')
# Name kanji not in jinmeiyo kanji list
valid_kanji.add('滕')
# Radical not in radicals list
valid_kanji = valid_kanji.union({'咼', '帀', '㠯', '𠂉', '𧘇', '卪'})

# 帀 composition 一 + ⼱

kanji = "鬱" # Most strokes in kanji&stroke
kanji = "食" # Most strokes in kanji&radicals
kanji = "駦" # First contraction found
kanji = "王" # Joyo kanji according to jisho, but not in kanji-svg database
kanji = "鹿" # Joyo kanji according to jisho, but not in kanji-svg database
lookup = kanji in valid_kanji
chinese = isKanji(realord(kanji)) # Check if kanji is real, does not mean it's used in japanese.
print(f"Is {kanji} in joyo kanji list? {lookup}")
print(f"Is {kanji} a Han character? {chinese}")

# Looks like some radicals have multiple unicode entries. Mapped with the .decomposition() function.
print(f"Is 亠 the same as ⼇? {'亠' == '⼇'}")
print('亠'.encode("unicode_escape"))
print('⼇'.encode("unicode_escape"))

# Looks like some characters look identical but are not the same unicode character. Unnecessary complexity for our purposes.
print(f"Is ㇁ the same as ㇓? {'㇁' == '㇓'}")
print('㇁'.encode("unicode_escape"))
print('㇓'.encode("unicode_escape"))

print(f'Is 扌 in radicals? {"扌" in radicals}')

weird_kanji = ['哀']

def reduce_parts(strokes: List[str]):
    # '醸' = ['酉', '六', '一', '㇑*', '㇑*', '一', '一', '㇒*', '㇙*', '㇒*', '㇏*'] => ['酉', '六', '一', '㇑*', '㇑*', '二', '𧘇']
    rules = [
        ('㇐*', '一'), # ㇐* => 一 simplifies rules
        ('㇑*', '㇑'), # ㇐* => 一 simplifies rules
        ('一,巾','帀'),
        ('㇒*,㇙*,㇒*,㇏*', '𧘇'),
        ('㇑,㇑,㇔*,㇒*,一', '业'),
        ('㇕*,一,一', '彐'),
        ('一,㇑,㇑,㇑,㇑', '卌'),
        ('一,㇑,㇑,㇑', '卅'),
        ('一,㇑,㇑', '卄'),
        ('一,一,一', '三'),
        ('一,一', '二'),
        ('㇒*,㇑,㇒*,㇔*', '𧘇'),
        ('㇑,㇕*,一,㇕*,一', '㠯'),
        ('㇑,㇕*,㇔*', '卪'),
        ('㇔*,㇒*', '丷'),
        
        # Questionable rules
        ('丿,丶', '冫'), # Technically correct, could lead to more issues down the line...
        
        # Probably bad rules
        # ('艹', '卄'), # They look the same :D
        ('㇂*,丿,丶', '义'), # Missing hook, not a huge fan of this one.
        ('㇂*,㇒*,㇔*', '义'), # Missing hook, not a huge fan of this one.
        ('㇒*,㇏*', '𠆢'), 
        # ('𠆢', '人'), 
    ]
    strokes_str = ','.join(strokes)
    for (match, result) in rules:
        
        # normalize the rules
        # match = "".join(map(lambda c : to_homoglyph(c), match))
        # result = "".join(map(lambda c : to_homoglyph(c), result))
        
        if match in strokes_str:
            strokes_str = strokes_str.replace(match, result)
    
    # Split and remove empty strings
    return list(filter(lambda c: c, strokes_str.split(',')))


def get_components(kanji_obj, depth = 0, joyo = True):
    ''' Recursively move down the tree until you find a joyo kanji, radical or stroke. Returns a list of components.
    '''
    
    # If we have reached a stroke without hitting a kanji, return the stroke
    if type(kanji_obj) is Stroke:
        return [f"{kanji_obj.stype[0]}*"] # stroke typically (type, connection)

    # Unless we are at the top level, we want to add the current kanji to the list of parts
    isComplete = kanji_obj.part is None
    # isPartial =  kanji_obj.partial == "true"

    if (depth != 0 and isComplete):
        elem = to_homoglyph(kanji_obj.element)
        isRadical   = elem in radicals
        isKanji     = elem in valid_kanji
        
        if isKanji or (isRadical and not joyo):
            return [elem]
        
        # NOTE: regarding kanji_obj.original
        # Using the kanji_obj.original might reduce the number of radicals to learn, however
        # - Original character is not necessary a used kanji.
        # - May have different stroke order / strokes amount, confusing learners.
    
    result = []
    for child in kanji_obj.childs:
        result.extend(get_components(child, depth + 1, joyo))
    return result

# Look up all joyo kanji in the kanji-svg database
kanji_parts = {}
kanji_dict = {}
svg_file_list = listSvgFiles("./kanji/")
for kanji in joyo_kanji:
    kanji_id = canonicalId(kanji)
    svg_files = [(f.path, f.read()) for f in svg_file_list if f.id == kanji_id]
    path, kanji_info = svg_files[0] # Select the first one
    kanji_strokes = kanji_info.strokes
    kanji = kanji_strokes.element

    comp_from_VG = kanji_strokes.components(recursive=True)
    comp_without_radicals = get_components(kanji_strokes)
    comp_with_radicals = reduce_parts(get_components(kanji_strokes, joyo = False))

    kanji_parts[kanji] = comp_without_radicals
    kanji_dict[kanji] = {
        'comp_kanji': [kanji for kanji in comp_without_radicals if kanji in valid_kanji],
        'comp_kanji&radicals': comp_with_radicals, # Kanji, radicals and strokes
        'comp_kanji&strokes': comp_without_radicals, # Only kanji and strokes
        'comp_preferred': reduce_parts(comp_without_radicals if len(comp_without_radicals) < max_comps else comp_with_radicals),
    }

    kanji_parts[kanji] = comp_without_radicals
    # print(comp_elems)

# Calculate a dependency tree for each kanji
for kanji in kanji_parts:
    # if kanji == "楼":
    #     print(f"{kanji} has {len(parts)} parts")

    kanji_dict[kanji] = {
        'part_of': [parent for parent, p_parts in kanji_parts.items() if kanji in p_parts],
    } | kanji_dict[kanji]

    print(f"{kanji} part of {kanji_dict[kanji]['part_of']}, contains {kanji_dict[kanji]['comp_kanji']}, radicals {kanji_dict[kanji]['comp_kanji&radicals']}, strokes {kanji_dict[kanji]['comp_kanji&strokes']}")

# How many have more than 'max_comps' components?
radical_comps = [
    (
        kanji,
        kanji_dict[kanji]['comp_preferred'],
        len(kanji_dict[kanji]['comp_preferred']),
    )
    for kanji in joyo_kanji
]
above_x_comps = list(filter(lambda x: x[2] > max_comps, radical_comps))
print(f"More than {max_comps} components: {len(above_x_comps)}")
for kanji, comps, num_comps in above_x_comps:
    print(f"{kanji} has {num_comps} components: {comps}")

# Manually group certain strokes together to reduce the number of components
kanji_dict['食'] = kanji_dict['食'] | { 'comp_preferred': (["𠆢"] + (kanji_dict['食']['comp_preferred'][2:]))}



        


# Ideally we want to minimize the amount of radicals the user will have to learn, since they are not kanji themselves.
# given 'max_comps', how many radicals will the user encounter?
seen_strokes = set()
seen_radicals = set()
seen_other = set()
seen_name_kanji = set()
for kanji in joyo_kanji:
    for part in kanji_dict[kanji]['comp_preferred']:
        if part not in joyo_kanji:
            if '*' in part: 
                seen_strokes.add(part[:-1])
            elif part in radicals:
                seen_radicals.add(part)
            elif part in jinmeiyo_kanji:
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
print(len(joyo_kanji))