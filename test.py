import unittest

from my_code.kanjivg_utils import comps_from_tree, get_comp_list_recursive, load_kanji, reduce_comps

class TestCompTree(unittest.TestCase):
    def get_kanji_comps(self, kanji):
        comp_list = self.get_kanji_comp_tree(kanji)
        return comps_from_tree(comp_list)

    def get_kanji_comp_tree(self, kanji):
        kanji_obj = load_kanji(kanji)
        comp_list = get_comp_list_recursive(kanji_obj)
        comp_list = reduce_comps(comp_list)
        return comp_list

    def test_形(self):
        comps = self.get_kanji_comps('形')
        self.assertEqual(['开', '⼺'], comps)
        
    def test_臣(self):
        comps = self.get_kanji_comps('臣')
        self.assertEqual(['㇑', '丅', 'コ','丄'], comps)
        
    def test_哀(self):
        comps = self.get_kanji_comps('哀')
        self.assertEqual(['⼇', '口', '𧘇'], comps)
        
    def test_鬱(self):
        comps = self.get_kanji_comps('鬱')
        self.assertEqual(['缶', '木', '木', '⼍', '⾿', '⼺'], comps)
        
    def test_食(self):
        comps = self.get_kanji_comps('食')
        self.assertEqual(['人', '良'], comps)

    def test_王(self):
        comps = self.get_kanji_comps('王')
        self.assertEqual(['丅', '二'], comps)

    def test_鹿(self):
        comps = self.get_kanji_comps('鹿')
        self.assertEqual(['⼴', '㇕', '⿚', '比'], comps)
        
    # def test_駦(self):
    #     comps = self.get_kanji_comps('駦')
    #     self.assertEqual(['⼴', '㇕', 'ᚇ', '比'], comps)
    
    def test_咼(self):
        comps = self.get_kanji_comps('咼')
        self.assertEqual(['⿙', '㇑', '一', '⼌', '口'], comps)
    
    def test_良(self):
        tree = self.get_kanji_comps('良')
        self.assertEqual(['㇔', '⾉'], tree)
    
    def test_繊(self):
        tree = self.get_kanji_comps('繊')
        self.assertEqual(['糸', '土', '业', '㇂', '冫'], tree)
    
    def test_卵(self):
        # Box radical wrong stroke order
        tree = self.get_kanji_comps('卵')
        self.assertEqual(['⼕', 'ン', '㇆', '丶', '㇑'], tree)
    
    def test_a1(self):
        # Box radical wrong stroke order
        tree = self.get_kanji_comps('籠')
        self.assertEqual(['𥫗', '立', '月', '⺊', '己', '三'], tree)
    
    # def test_huh(self):
    #     comps = self.get_kanji_comps('⾉')
    #     self.assertEqual(['㇑', '⾉'], comps)
        
    # 帀 composition 一 + ⼱

if __name__ == '__main__':
    unittest.main()
    

# lookup = kanji in get_valid_kanji()
# chinese = isKanji(realord(kanji)) # Check if kanji is real, does not mean it's used in japanese.
# print(f"Is {kanji} in joyo kanji list? {lookup}")
# print(f"Is {kanji} a Han character? {chinese}")

# # Looks like some radicals have multiple unicode entries. Mapped with the .decomposition() function.
# print(f"Is 亠 the same as ⼇? {'亠' == '⼇'}")
# print('亠'.encode("unicode_escape"))
# print('⼇'.encode("unicode_escape"))

# # Looks like some characters look identical but are not the same unicode character. Unnecessary complexity for our purposes.
# print(f"Is ㇁ the same as ㇓? {'㇁' == '㇓'}")
# print('㇁'.encode("unicode_escape"))
# print('㇓'.encode("unicode_escape"))

# print(f'Is 扌 in radicals? {"扌" in radicals}')