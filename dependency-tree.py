## An attempt to create a dependency tree including all JoYo kanji based on their parts.
import csv

from utils import canonicalId, listSvgFiles

kanji_id = canonicalId("食")
svg_files = listSvgFiles("./kanji/")
kanji_svg_files = [(f.path, f.read()) for f in svg_files if f.id == kanji_id][0]

kanji_id = canonicalId("亜")
svg_files = listSvgFiles("./kanji/")
kanji_svg_files = [(f.path, f.read()) for f in svg_files if f.id == kanji_id][0]

# Create list of all joyo-kanji
joyo_kanji_list = []
with open("my_files/joyo2010.tsv", "r", encoding="utf8") as kanji_file:
    tsv_reader = csv.reader(kanji_file, delimiter="\t")

    # Skip the first row, which is the header
    next(tsv_reader)

    for row in tsv_reader:
        (kanji, old_kanji, strokes, school_grade, added, reading) = row
        joyo_kanji_list.append(kanji)
        print(f"{kanji} has {strokes} strokes")
        
# Look up all joyo kanji in the kanji-svg database
for kanji in joyo_kanji_list:
    kanji_id = canonicalId(kanji)
    svg_files = [(f.path, f.read()) for f in listSvgFiles("./kanji/") if f.id == kanji_id]
    svg_file = svg_files[0]
    
print(len(joyo_kanji_list))