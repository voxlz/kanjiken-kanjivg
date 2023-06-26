# Create list of all joyo-kanji
import csv

from my_code.unicode import to_homoglyph


def get_joyo_kanji():
    '''Returns a list of all joyo-kanji'''
    joyo_kanji_list = set()
    with open("my_files/joyo2010.tsv", "r", encoding="utf8") as kanji_file:
        tsv_reader = csv.reader(kanji_file, delimiter="\t")

        # Skip the first row, which is just the source link
        next(tsv_reader)

        for row in tsv_reader:
            (kanji, old_kanji, radical_comps, school_grade, added, reading) = row
            joyo_kanji_list.add(to_homoglyph(kanji))
    return joyo_kanji_list

def get_jinmeiyo_kanji():
    '''Returns a list of all jinmeiyo-kanji'''
    jinmeiyo_kanji_list = set()
    with open("my_files/jinmeiyo.csv", "r", encoding="utf8") as kanji_file:
        tsv_reader = csv.reader(kanji_file, delimiter=",")

        # Skip the first row, which is just the source link
        next(tsv_reader)

        for row in tsv_reader:
            (kanji, *variant) = row
            jinmeiyo_kanji_list.add(to_homoglyph(kanji))
            if variant != []: jinmeiyo_kanji_list.add(to_homoglyph(variant[0]))
    return jinmeiyo_kanji_list