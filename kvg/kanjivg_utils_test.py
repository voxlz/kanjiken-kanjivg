

import unittest
from kanjivg import Stroke

from my_code.kanjivg_utils import check_for_stroke, comps_from_tree, get_comp_list_recursive, get_comps_depth, load_kanji, reduce_comps

class TestUtils(unittest.TestCase):

    def test_isStroke(self):
        kanji_obj = Stroke({})
        kanji_obj.stype = '㇔'
        kanji_obj.svg = 'M17.71,16.59c2.46,2.07,6.36,8.49,6.98,11.71'        

        isStroke, stroke = check_for_stroke(kanji_obj)
        self.assertEqual(isStroke, True)
        self.assertEqual(stroke, '㇔')
    
    # Make sure it does not reduce itself
    def test_reduce_self(self):
        char  = '十'
        kanji_obj = load_kanji(char)
        comps = get_comp_list_recursive(kanji_obj)
        comps = reduce_comps(comps, char)
        self.assertEqual(comps, ['㇐', '㇑'])
        
    def test_depth(self):
        a = ['㇐', {'口': ['㇐']}, {'\u2fda': ['㇐']}]
        self.assertEqual(get_comps_depth(a), 2)
        
        b = [{'AA': ['㇐', {'口': ['㇐']}, {'\u2fdb': ['㇐']}]}]
        self.assertEqual(get_comps_depth(b), 3)
        

if __name__ == '__main__':
    unittest.main()
    