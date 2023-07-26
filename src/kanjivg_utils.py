import os
from kvg.kanjivg import Stroke
from src.reduction import get_rules
from src.tree import Tree
from src.unicode import get_radicals, get_strokes, get_valid_kanji, to_homoglyph
from kvg.utils import canonicalId, listSvgFiles
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

svg_file_list = listSvgFiles(os.path.abspath("./kanji /"))

def load_kanji(kanji):
    ''' Load the kanji from the kanji-svg database. '''
    kanji_id = canonicalId(kanji)
    kanji_info = [f.read() for f in svg_file_list if f"{kanji_id}.svg" in f.path][0]
        
    return kanji_info.strokes

def check_for_stroke(kanji_obj):
    ''' Check if the kanji_obj is a stroke. '''
    isStroke = False
    stroke = None
    
    # Stroke is the innermost element, return it as is
    if type(kanji_obj) is Stroke:
        stroke = f"{to_homoglyph(kanji_obj.stype[0])}"
        isStroke = True
    elif (stroke := to_homoglyph(kanji_obj.element)) in get_strokes():
        isStroke = True
    
    return isStroke, stroke

# def get_comp_list(kanji_obj, depth = 0):
#     ''' Recursively move down the tree until you find a joyo kanji, radical or stroke. Returns a list of components.
#     '''
    
#     # Stroke is the innermost element, return it as is
#     isStroke, stroke = check_for_stroke(kanji_obj)
#     if isStroke: return [stroke]
        
#     isComplete = kanji_obj.part is None
#     element = to_homoglyph(kanji_obj.element)
    
#     if (depth != 0 and isComplete):
#         isRadical   = element in get_radicals()
#         isKanji     = element in get_valid_kanji()
        
#         if isKanji or isRadical:
#             return [element]
    
#     result = []
#     for child in kanji_obj.childs:
#         result.extend(get_comp_list(child, depth + 1))
#     return result

def get_comp_list_recursive(kanji_obj):
    ''' Recursively creates an list of components for a kanji. '''

    result = []
    for child in kanji_obj.childs:
        child_comps = Tree()
        
        # Stroke is the innermost element, return it as is
        isStroke, stroke = check_for_stroke(child)
        if isStroke: 
            result.append(stroke)
            continue
                
        comp_tree  = get_comp_list_recursive(child)
        strokes     = get_strokes_from_comps(comp_tree)
        element      = to_homoglyph(child.element)

        # Some things must be true for the element to be valid
        isExistent   = element is not None
        isComplete   = child.part is None
        isPartial     = child.partial == "true"
        isCOMPLETE   = isExistent and isComplete and not isPartial 
        
        # Then, if the element is a radical or joyo kanji, it is valid
        isRadical  = element in get_radicals()
        isKanji      = element in get_valid_kanji()
        isKANJI      = isRadical or isKanji
        
        # Else, if not curriculum, check for red flags 
        # isVariant    = child.variant == "true" # This is inconsistent.
        # isOriginal   = child.original is None
        # isRadical    = child.radical is not None
        # isUNICODE    = not (isVariant and isOriginal) 
        
        # if not (isCOMPLETE and isKANJI) and element is not None and kanji_obj.element is not None and isComplete:
        #     print(f"Skipping {element} from {kanji_obj.element}")
        
        # If valid, add current element to the list of components
        if isCOMPLETE and (isKANJI):
            child_comps[element] = reduce_comps(comp_tree, element)
            result.append(child_comps)
        # If not a valid character, skip and go down the tree
        else:
            result.extend(comp_tree)
    return result

def comps_from_tree(comp_tree):
    ''' Get the direct components of this kanji-comp tree. 
    [{'开': [...]}, {'⼺': [...]}] -> ['开', '⼺']'''
    
    return list(map(lambda x: x if type(x) is str else list(x.keys())[0], comp_tree))

def simplify_comp_list(comp_tree):
    ''' Get the direct child components from component tree. '''
    
    rtn = []
    # Either recursive tree or a stroke string
    for char in comp_tree:
        if type(char) is str:
            rtn.append(char)
        else:
            rtn.append(list(char.keys())[0])
    return rtn

def expand_comps(comps, char_dict):
    ''' Takes a simplified comps list and expands it using char_dict. Ensures consistency.'''
    
    rtn = []
    # Either recursive tree or a stroke string
    for char in comps:
        if char in char_dict:
            if (char_comp := char_dict[char]['comps']) == []:
                rtn.append(char)
            else:
                rtn.append({char: expand_comps(char_comp, char_dict)})
    return rtn

def get_strokes_from_comps(comps):
    ''' '''
    rtn = []
    for char in comps:
        if type(char) is str:
            rtn.append(char)
        else:
            rtn.extend(get_strokes_from_comps(char[list(char.keys())[0]]))
    return rtn

def set_strokes_parents_depth(char, char_dict):
    ''' Return comp list with strokes only recursively. '''
    
    comps = expand_comps(char_dict[char]['comps'], char_dict)
    
    set_parents(char, comps, char_dict)
    strokes = get_strokes_from_comps(comps)
    depth = 1 + get_comps_depth(comps)
    
    char_dict[char] |= { 'strokes': strokes, 'depth': depth}

def get_lvl_str(comp_tree):
    ''' Get the top most string representation of a component tree. '''
    
    return ",".join(simplify_comp_list(comp_tree))

def reduce_comps(comp_list, from_char, do_not_deduce_to=None):
    ''' Recursively reduce a list of components. Works on both recursive and non-recursive component lists. '''
        
    # Apply applicable reduction rules to comp_list
    reduction_rules, do_not_reduce = get_rules()

    # * Don't reduce if less than 4 strokes
    strokes = get_strokes_from_comps(comp_list)
    if len(strokes) < 5:
        return strokes

    # * Don't reduce if character is banned from reduction
    if from_char in do_not_reduce:
        return comp_list

    for rule, result in reduction_rules:

        # to avoid bad replacements
        result = to_homoglyph(result)

        # Skip if rule is not a valid reduction
        if result in [from_char, do_not_deduce_to]: 
            continue 

        # Replace if rule is a reduction
        lvl_comps_str = ",".join(simplify_comp_list(comp_list))
        while (str_index := lvl_comps_str.find(rule)) != -1:
            itm_index = lvl_comps_str.count(',', 0, str_index)
            rule_len = rule.count(',') + 1
            sliced = slice(itm_index,itm_index+rule_len)
            if rule_len > 1:
                comp_list[sliced] = [{result: comp_list[sliced]}]
            elif type(comp_list[itm_index]) is str:
                comp_list[itm_index] = result
            else:
                comp_list[itm_index] = {result: comp_list[itm_index][rule]}
            lvl_comps_str = ",".join(simplify_comp_list(comp_list))


    # Recursively go down the component tree
    for i, comp in enumerate(comp_list):
        if type(comp) is str:
            continue
        for char, comp_tree in comp.items():
            comp_list[i] = {char: reduce_comps(comp_tree, char)}


    return comp_list

def count_occurrences(comps_recursive, char_dict, kanji):
    ''' Recursively find and count all components in a kanji. '''
    
    # Recursively go down the component tree
    for comp in comps_recursive:
        if type(comp) is str:
            char = comp
            if char in char_dict:
                update = {
                    'occur': char_dict[char]['occur'] + 1,
                    'derived': char_dict[char]['derived'] | {kanji},
                }
                char_dict[char] = char_dict[char] | update
            else:
                char_dict[char] = {
                    'comps'  : [],   # The components of the character
                    'from'   : kanji,  # Character that this component is originally from
                    'general'      : {
                        'group' : "stroke"       # type: joyo, jinmeiyo, radical, stroke, hyougai
                    },
                    'occur'  : 1,      # How often this char occurs as a comp, including itself
                    'n_comps': 0,
                    'derived': {kanji}, # Kanji 
                    'parent': set(),   # Kanji this character occurs in directly
                }
        else:
            char = list(comp.keys())[0]
            if char in char_dict:
                update = {
                    'occur': char_dict[char]['occur'] + 1,
                    'derived': char_dict[char]['derived'] | {kanji},
                }
                char_dict[char] = char_dict[char] | update
            else:
                comps = reduce_comps(comp[char], char)
                comps = simplify_comp_list(comps) # 
                isRadical = char in get_radicals()
                group = "radical" if isRadical else "hyougai"
                char_dict[char] = {
                    'comps'  : comps, # The comps of the char
                    'from'   : kanji,  # Char that this comp is originally from
                    'general' : {
                        'group' : group,  # joyo, jinmeiyo, radical, stroke, hyougai
                    },
                    'occur'  : 1,  # How often this char occurs as a comp, including itself
                    'n_comps': len(comp[char]),
                    'derived': {kanji}, # Chars this char occurs in
                    'parent': set(),  # Char the curr char is a direct component of
                }
            
            # Recursively count occurrences of this component
            count_occurrences(comp[char], char_dict, kanji)
    
    return char_dict

# TODO: Probably ignore order of components
def find_twins(char_a, char_dict):
    ''' Find all characters that have the same components. '''
    twins = set()
    for char_b in char_dict:
        if char_a == char_b: continue
        
        isNotStroke = char_dict[char_a]['comps'] != []
        match = char_dict[char_a]['comps'] == char_dict[char_b]['comps']
        if isNotStroke and match:
            twins.add(char_b)
        
    char_dict[char_a] |= {'twins': twins}
    


def set_parents(parent, comps, char_dict):
    
    for char in comps:
        if type(char) == dict:
            child, child_comps = next(iter(char.items()))
            char_dict[child]['parent'] |= {parent}
            set_parents(child, child_comps, char_dict)
        else:
            char_dict[char]['parent'] |= {parent}
    

def get_comps_depth(comps):
    ''' Calculates the depth of a [{}, ''] comp tree. Essentially counts the amount of nested brackets. '''
    
    depth = [0]
    for char in comps:
        if type(char) == dict:
            c_comps = next(iter(char.values()))
            depth.append(1 + get_comps_depth(c_comps))
        if type(char) == str:
            depth.append(1)
        
    return max(depth)
    
def find_similar(char_a, char_dict):
    ''' Find all characters that have the same components. '''
    
    similar_lst = []
    for char_b in char_dict:
        if char_a == char_b: continue

        a_comps     = "".join(char_dict[char_a]['comps'])
        b_comps     = "".join(char_dict[char_b]['comps'])
        if a_comps != "" and b_comps != "":
            a_strokes = "".join(char_dict[char_a]['strokes'])
            b_strokes = "".join(char_dict[char_b]['strokes'])
            score = similar(a_comps, b_comps) + similar(a_strokes, b_strokes)
            similar_lst.append((char_b, score))

    update = {
        'similar': list(reversed(sorted(similar_lst, key=lambda x: x[1])[-10:]))
    }

    char_dict[char_a] |= update