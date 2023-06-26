# Convert string unicode to char
from ast import literal_eval
import csv

# Convert string unicode to char
str_unicode = "0x" + "2ED0"
convert_str = literal_eval(str_unicode)
non_standard = chr(convert_str)

# Convert string unicode to char
str_unicode = "0x" + "2ED0"
convert_str = literal_eval(str_unicode)
non_standard = chr(convert_str)

# Convert string unicode to char
str_unicode = "2ED0"
convert_str = int(str_unicode, 16)
non_standard = chr(convert_str)

def to_chr(unicode_codepoint):
    ''' Convert string unicode to char: 2ED0 -> ⻐'''
    return chr(int(unicode_codepoint, 16))

homo_dict = {} 
def to_homoglyph(char):
    ''' Convert characters to their default homoglyph unicode representation. This is needed as some radicals have multiple unicode representations. '''
    
    # Create mapping
    if homo_dict == {}:
        with open("my_files/homoglyphs.csv", "r", encoding="utf8") as mapping:
            reader = csv.reader(mapping, delimiter=",")

            # Skip the first rows, which is just the source link
            for _ in range(9): next(reader)

            
            for row in reader:
                if '#' in row[0]: continue
                (normal_rep, *homoglyphs) = row
                for homoglyph in homoglyphs:
                    homo_dict[
                        to_chr(homoglyph)
                    ] = to_chr(normal_rep)
    
    # Lookup the character
    return homo_dict[char] if char in homo_dict else char
