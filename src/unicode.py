# Convert string unicode to char
from ast import literal_eval
import csv

from sortedcollections import OrderedSet

from src.radicals import get_radicals, get_strokes

def to_chr(unicode_codepoint):
    ''' Convert string unicode to char: 2ED0 -> ⻐'''
    return chr(int(unicode_codepoint, 16))

file_jouyou = OrderedSet()
def get_joyo_kanji():
    '''Returns a list of all joyo-kanji from disk'''
    
    # If already in memory, use that.
    if file_jouyou != set(): 
        return file_jouyou
        
    with open("data/joyo2010.tsv", "r", encoding="utf8") as kanji_file:
        reader = csv.reader(kanji_file, delimiter="\t")

        # Skip the first row, which is just the source link
        next(reader)

        for row in reader:
            (kanji, *_) = row
            file_jouyou.add(kanji)
    return file_jouyou

jinmeiyo = OrderedSet()
def get_jinmeiyo_kanji():
    '''Returns a list of all jinmeiyo-kanji'''
    
    # If already in memory, use that.
    if jinmeiyo != set(): 
        return jinmeiyo
    
    with open("data/jinmeiyo.csv", "r", encoding="utf8") as kanji_file:
        tsv_reader = csv.reader(kanji_file, delimiter=",")

        # Skip the first row, which is just the source link
        next(tsv_reader)

        for row in tsv_reader:
            (kanji, *variant) = row
            jinmeiyo.add(kanji)
            if variant != []: jinmeiyo.add(variant[0])
    return jinmeiyo

def get_hyougai_kanji():
    ''' Kanji that appear in the kanji-svg database / are useful radicals but are not in the joyo kanji list '''
    hyougai =  {
        '廌','兹','开','并','滕','咼','帀','㠯','𠂉','𧘇','卪','丆','囬','⺈','𠂊','⿚','𠀉','𧰨','𠀎','朿','龶','玄','丅','コ','丄','业','ン','𥫗', '𠚍', '㐅', '𠁼', '龹', '飠'
    }
    
    return map(lambda x: to_homoglyph(x), hyougai)

valid = OrderedSet()
def get_valid_kanji():
    '''Returns a list of all valid kanji'''
    
    global valid

    if not valid:
        valid = get_joyo_kanji() | get_jinmeiyo_kanji() | get_hyougai_kanji()
        
    return valid

homo_dict = {} 
def to_homoglyph(char):
    ''' Convert characters to the preferred default homoglyph unicode representation. This is needed as some radicals have multiple unicode representations. 
    
    The preferred order goes like this:
    1. Stokes (first to ensure '一' encodes properly)
    2. Joyo Kanji
    3. Radicals
    4. Jinmeiyo Kanji 
    '''
    
    # Create mapping
    if homo_dict == {}:
        with open("data/homoglyphs.csv", "r", encoding="utf8") as mapping:
            reader = csv.reader(mapping, delimiter=",")

            strokes = get_strokes()
            joyo = get_joyo_kanji()
            radicals = get_radicals()
            jinmeiyo = get_jinmeiyo_kanji()

            for row in reader:
                if '#' in row[0]: continue # Skip if comment
                row = list(map(to_chr, row))

                prefer = None # Preferred representation

                # Check for joyo chars
                prefer = find_in_char_set(strokes, row, prefer)
                prefer = find_in_char_set(joyo, row, prefer)
                prefer = find_in_char_set(radicals, row, prefer)
                prefer = find_in_char_set(jinmeiyo, row, prefer)

                if prefer is None:
                    continue
                for alt_char in [c for c in row if c != prefer]:
                    homo_dict[alt_char] = prefer

    # Lookup the character
    char = homo_dict[char] if char in homo_dict else char
    
    
    
    return char

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
