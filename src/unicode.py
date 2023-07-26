# Convert string unicode to char
from ast import literal_eval
import csv
import functools
from pickle import MEMOIZE
import re

from sortedcollections import OrderedSet

def to_chr(unicode_codepoint):
    ''' Convert string unicode to char: 2ED0 -> ⻐'''
    return chr(int(unicode_codepoint, 16))

@functools.cache
def get_joyo():
    '''Returns a list of all joyo-kanji from disk'''
    file_jouyou = OrderedSet()

    with open("data/joyo2010.tsv", "r", encoding="utf8") as kanji_file:
        reader = csv.reader(kanji_file, delimiter="\t")

        # Skip the first row, which is just the source link
        next(reader)

        for row in reader:
            (kanji, *_) = row
            file_jouyou.add(kanji)
    return file_jouyou

@functools.cache
def get_jinmeiyo():
    '''Returns a list of all jinmeiyo-kanji'''
    jinmeiyo = set()
    
    with open("data/jinmeiyo.csv", "r", encoding="utf8") as kanji_file:
        tsv_reader = csv.reader(kanji_file, delimiter=",")

        # Skip the first row, which is just the source link
        next(tsv_reader)

        for row in tsv_reader:
            (kanji, *variant) = row
            jinmeiyo.add(kanji)
            if variant != []: jinmeiyo.add(variant[0])
    
    return jinmeiyo.difference(get_joyo(), get_strokes())

@functools.cache
def get_hyougai_kanji():
    ''' Kanji that appear in the kanji-svg database / are useful radicals but are not in the joyo kanji list '''
    hyougai =  {
        '廌','兹','开','并','滕','咼','帀','㠯','𠂉','𧘇','卪','丆','囬','⺈','𠂊','𠀉','𧰨','𠀎','朿','龶','玄','丅','コ','丄','业','ン','𥫗', '𠚍', '㐅', '𠁼', '龹', '飠'
    }
    
    return map(lambda x: to_homoglyph(x), hyougai)

@functools.cache
def get_valid_kanji():
    '''Returns a list of all valid kanji'''
    return get_joyo() | get_jinmeiyo() | get_hyougai_kanji()

@functools.cache
def load_pref_homoglyph():
    pref_homo = {}
    
    with open("data/homoglyphs.csv", "r", encoding="utf8") as mapping:
        reader = csv.reader(mapping, delimiter=",")

        strokes = get_strokes()
        joyo = get_joyo()
        radicals = get_radicals()
        jinmeiyo = get_jinmeiyo()

        for row in reader:
            if '#' in row[0]: continue # Skip if comment
            row = list(map(to_chr, row))

            # Preferred representation
            prefer = None 

            # Check for joyo chars
            prefer = find_in_char_set(strokes, row, prefer)
            prefer = find_in_char_set(joyo, row, prefer)
            prefer = find_in_char_set(jinmeiyo, row, prefer)
            prefer = find_in_char_set(radicals, row, prefer) # Not used in real words, should be low prio
           
            # xi radical encoding not in jp dictionaries, avoid them.
            
            if prefer is None:
                continue
            for alt_char in [c for c in row if c != prefer]:
                pref_homo[alt_char] = prefer
                
    return pref_homo

@functools.cache
def load_homo_dict():
    ''' Load Homoglyphs '''
    other_homo = {}
    
    with open("data/homoglyphs.csv", "r", encoding="utf8") as f:
        reader = csv.reader(f, delimiter=",")

        for row in reader:
            if '#' in row[0]: continue # Skip if comment
            row = list(map(to_chr, row))

            # Save homoglyphs
            for char in row:
                other_homo[char] = row
    return other_homo
                
def to_homoglyph(char):
    ''' Convert characters to the preferred default homoglyph unicode representation. This is needed as some radicals have multiple unicode representations. 
    
    The preferred order goes like this:
    1. Stokes (first to ensure '一' encodes properly)
    2. Joyo Kanji
    3. Radicals
    4. Jinmeiyo Kanji 
    '''
    
    # Create mapping
    pref_homo = load_pref_homoglyph()

    # Lookup the character
    char = pref_homo[char] if char in pref_homo else char
    
    return char

def get_homoglyphs(char):
    other_homo = load_homo_dict()
    return other_homo[char] if char in other_homo else [char]

def find_in_char_set(char_set, homoglyphs, prefer):
    ''' Unless we already prefer another char, loop through homoglyphs and return the one in the desired char_set'''
    if prefer is None:
        for homoglyph in homoglyphs:
            if homoglyph in char_set:
                if prefer is None:
                    prefer = homoglyph
                else:
                    raise LookupError("Multiple chars from same char-set considered homoglyphs")
    return prefer

def find_not_in_char_set(char_set, homoglyphs, prefer):
    ''' Select first char not in char_set'''
    if prefer is None:
        for homoglyph in homoglyphs:
            if homoglyph not in char_set and prefer is None:
                prefer = homoglyph
                break
    return prefer

kanji_block = r"[\u4E00-\u9FFF]"

@functools.cache
def get_radicals():
    '''Returns a list of all radicals'''
        
    # If already in memory, use that.
    radicals = set()
    
    with open("data/radicals_kangxi.csv", "r", encoding="utf8") as radical_file:
        reader = csv.reader(radical_file)

        for row in reader:
            if "#" in row[0]: continue # Skip if comment
            radical = row[0]
            
            # Prefer Kanji representation (XI not in jp dictionaries)
            radical_alts = get_homoglyphs(radical)
            alt = [c for c in radical_alts if  re.search(kanji_block, c)]

            radicals.add(alt[0] if alt else radical)
    
        # Add my custom radicals
        radicals = radicals.union({'⿗', '⿖', '⿚', '⿘'} )
            
    return radicals.difference(get_joyo(), get_strokes(), get_jinmeiyo())

@functools.cache
def get_strokes():
    '''Returns a list of all strokes'''
    CJK_strokes = set()
    
    with open("data/strokes.csv", "r", encoding="utf8") as file:
        reader = csv.reader(file)

        for row in reader:
            if "#" in row[0]: continue # Skip if comment
            radical = row[0]
            CJK_strokes.add(radical)
            
    return CJK_strokes.difference(get_joyo())

def remove_duplicates(char_set, name):
    ''' Remove homoglyph duplicates from a set of
    characters with to_homoglyph. '''
    
    old_len = len(char_set)
    pref_chars = set(map(to_homoglyph, char_set))
    char_set = pref_chars.intersection(char_set)
    # removed = pref_chars.difference(char_set)
    print(f"{name}: {old_len} -> {len(char_set)} (-{old_len - len(char_set)})")
    return char_set