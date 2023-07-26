from src.tree import Tree


def set_kanken(char_dict):
    ''' Set kanken grade for each character in char_dict.'''
    
    # Load kanken data from file
    with open('data/nihongo-pro.com/kanken.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
        kanken = Tree()
        curr_lvl = 10
        for line in lines:
            line = line.strip()
            if line == "": continue
            elif line.startswith("Level"):
                curr_lvl = float(line.split(":")[0].split(" ")[-1])
            else:
                kanken[curr_lvl] = line.split(" ")
    
    for char in char_dict:
        for lvl, kanji_list in kanken.items():
            if char in kanji_list:
                char_dict[char]['general']['kanken'] = lvl
                break