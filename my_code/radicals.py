import csv


def get_radicals():
    '''Returns a list of all radicals'''
    kangxi_radicals = set()
    
    # If already in memory, use that.
    if kangxi_radicals != set(): 
        return kangxi_radicals
    
    with open("my_files/radicals_kangxi.csv", "r", encoding="utf8") as radical_file:
        reader = csv.reader(radical_file)

        for row in reader:
            if "#" in row[0]: continue # Skip if comment
            radical = row[0]
            kangxi_radicals.add(radical)
    
        # Add my custom radicals
        kangxi_radicals = kangxi_radicals.union({'⿗', '⿖'} )
            
    return kangxi_radicals

CJK_strokes = set()
def get_strokes():
    '''Returns a list of all strokes'''
    
    # If already in memory, use that.
    if CJK_strokes != set(): 
        return CJK_strokes
    
    with open("my_files/strokes.csv", "r", encoding="utf8") as file:
        reader = csv.reader(file)

        for row in reader:
            if "#" in row[0]: continue # Skip if comment
            radical = row[0]
            CJK_strokes.add(radical)
            
    return CJK_strokes


# ----- DEPRECATED -----

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