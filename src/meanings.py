import csv

from src.unicode import to_homoglyph


def set_char_meanings(char_dict):
    ''' Set the meanings of each character in char_dict. 
    Goals:
        1. No two char should have the same meaning to avoid confusion.
        2. Strokes should not have meanings.
        3. The meaning should be the most common meaning of the kanji.
        4. The meaning should be a single word (2 if there is no english equivalent).
    '''
    
    # Load the meanings from disk
    seen_meanings = set()
    meanings = {}
    with open("data/kanjialive/ka_data.csv", "r", encoding="utf8") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader) # skip header
        for row in reader:
            if '#' in row[0]: continue # Skip comments
            (kanji,name,stroke,meaning,grade,*_) = row
            kanji = to_homoglyph(kanji)
            
            if kanji in char_dict and kanji not in meanings:
                if (meaning != "" and meaning[0] == '"' and meaning[-1] == '"'):
                    meaning = meaning[1:-1]
                meaning = meaning.split(',')[0].strip()
                
                if meaning in seen_meanings:
                    print(f"Warning: duplicate meaning {meaning} for {kanji}")
                else:
                    seen_meanings.add(meaning)

                meanings[to_homoglyph(kanji)] = {'meaning': meaning, 'grade': grade}
            
    with open("data/kanjialive/japanese-radicals.csv", "r", encoding="utf8") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader) # skip header
        for row in reader:
            if '#' in row[0]: continue # Skip comments
            (id,stroke,radical,meaning,*_) = row
            radical = to_homoglyph(radical)
            
            if radical in char_dict and radical not in meanings:
                
                if (meaning != "" and meaning[0] == '"' and meaning[-1] == '"'):
                    meaning = meaning[1:-1]
                meaning =  meaning.split(',')[0].strip()
                    
                if meaning in seen_meanings:
                    print(f"Warning: duplicate meaning {meaning} for {radical}")
                else:
                    seen_meanings.add(meaning)    
        
                meanings[radical] = {'meaning': meaning, 'grade': 'n/a'}
                
    # Check for duplicate meanings
                
    print()
