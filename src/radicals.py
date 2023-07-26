import csv

from src.unicode import to_homoglyph


# ----- DEPRECATED -----

def hex_to_unicode_str(hex_str):
    return hex_str.replace("0x", "\\u").encode('utf-8').decode('unicode-escape')

radical_kanji_mapping = {}
with open("data/kanji_radical_mapping.csv", "r", encoding="utf8") as mapping:
    tsv_reader = csv.reader(mapping, delimiter=",")

    # Skip the first row, which is just the source link
    next(tsv_reader)

    for row in tsv_reader:
        (kanji, radical, *a) = row
        radical_kanji_mapping[hex_to_unicode_str(radical)] = hex_to_unicode_str(kanji)