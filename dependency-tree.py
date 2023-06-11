## An attempt to create a dependency tree including all JoYo kanji based on their parts.
import csv
from kanjivg import Stroke

from utils import canonicalId, listSvgFiles

svg_files = listSvgFiles("./kanji/")
kanji_id = canonicalId("食")
kanji_svg_files = [(f.path, f.read()) for f in svg_files if f.id == kanji_id][0]

kanji_id = canonicalId("亜")
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
    path, kanji_info = svg_files[0] # Select the first one
    svg_info = kanji_info.strokes
    kanji = svg_info.element
    components = svg_info.childs

    # Go in one depth and get components that make up the kanji
    comps = []
    for comp in components:
        if type(comp) is Stroke or comp.part is None:
            comps.append(comp)
        elif comp.childs is not None:
            comps.extend(comp.childs)

    # Extract the elements (subkanji) or strokes of the components
    comp_elems = []
    for comp in comps:
        if type(comp) is Stroke:
            comp_elems.append(f"{comp.stype[0]}*")
        elif comp.element is None:
            comps.extend(comp.childs)
        else:
            comp_elems.append(comp.element)

    if None in comp_elems:
        print(f"None in {kanji}")
    print(comp_elems)

print(len(joyo_kanji_list))