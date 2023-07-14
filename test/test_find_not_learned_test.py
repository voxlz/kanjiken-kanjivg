
import unittest

from src.order import find_not_learned_comps


class Test_Find_not_learned_comps(unittest.TestCase):
    
    char_dict2 = {
        'test': {
            'comps': ['a', 'b', 'c'],
            'book_occur': 230,
        },
        'a': {
            'comps': [],
            'book_occur': 1000,
        },
        'b': {
            'comps': [],
            'book_occur': 90,
        },
        'c': {
            'comps': [],
            'book_occur': 2000,
        },
    }
    
    not_learned = list(find_not_learned_comps('test', [], char_dict2, []))
    
    def test_ensure_sorted(self):
        self.assertListEqual(self.not_learned, ['c', 'a', 'b'])
    

if __name__ == '__main__':
    unittest.main()