# Create list of all joyo-kanji
import csv
from sortedcollections import OrderedSet

file_jouyou = OrderedSet()
def get_joyo_kanji():
    '''Returns a list of all joyo-kanji from disk'''
    
    # If already in memory, use that.
    if file_jouyou != set(): 
        return file_jouyou
        
    with open("my_files/joyo2010.tsv", "r", encoding="utf8") as kanji_file:
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
    
    with open("my_files/jinmeiyo.csv", "r", encoding="utf8") as kanji_file:
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
    return {
        '廌','兹','开','并','滕','咼','帀','㠯','𠂉','𧘇','卪','丆','囬','⺈','𠂊','⿚','𠀉','𧰨','𠀎','朿','龶','玄','丅','コ','丄','业','ン','𥫗', '𠚍', '㐅', '𠁼'
    }

valid = OrderedSet()

def get_valid_kanji():
    '''Returns a list of all valid kanji'''
    
    global valid

    if not valid:
        valid = get_joyo_kanji() | get_jinmeiyo_kanji() | get_hyougai_kanji()
        
    return valid