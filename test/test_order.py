import unittest

from src.order import find_not_learned_comps, init_queue, prioritize_learn_order

class TestCompTree(unittest.TestCase):
    
    learn_order2 = ['å', 'a', 'b','c']
    char_dict2 = {
        'a': {
            'comps': ['å'],
            'book_occur': 1000,
        },
        'b': {
            'comps': [],
            'book_occur': 90,
        },
        'c': {
            'comps': [],
            'book_occur': 80,
        },
        'å': {
            'comps': [],
            'book_occur': 4,
        },
        'ä': {
            'comps': [],
            'book_occur': 2,
        },
        'ö': {
            'comps': [],
            'book_occur': 2,
        },
    }
    
    # [b, å, a, c] => [b, c, å, a]
    # [90, 4, 100, 80] than [90, 80, 4, 100] => 
    # [90, 94, 194, 274] vs [90, 170, 174, 274]  => 
    # [0, -76, +20, 0] vs [0, +76, -20, 0] => 
    # Second is better. (less negative)
    rank_order = ['a', 'b', 'c']
    learn_order = ['b', 'c', 'å', 'a']
    char_dict = {
        'a': {
            'comps': ['å'],
            'book_occur': 100,
        },
        'b': {
            'comps': [],
            'book_occur': 90,
        },
        'c': {
            'comps': [],
            'book_occur': 80,
        },
        'å': {
            'comps': [],
            'book_occur': 4,
        },
        'ä': {
            'comps': [],
            'book_occur': 2,
        },
        'ö': {
            'comps': [],
            'book_occur': 2,
        },
    }
    
    #['a', 'c', 'd', 'ä', 'å', 'ö', 'b'] => ['a', 'c', 'd', 'ö', 'å', 'ä', 'b']
    rank_order3 = ['a', 'b', 'c', 'd']
    learn_order3 = ['a', 'c', 'd', 'ä', 'ö', 'å', 'b']
    char_dict3 = {
        'a': {
            'comps': [],
            'book_occur': 10000,
        },
        'b': {
            'comps': ['å', 'ö'],
            'book_occur': 1000,
        },
        'c': {
            'comps': [],
            'book_occur': 80,
        },
        'd': {
            'comps': [],
            'book_occur': 80,
        },
        'å': {
            'comps': [],
            'book_occur': 4,
        },
        'ä': {
            'comps': [],
            'book_occur': 6,
        },
        'ö': {
            'comps': ['ä'],
            'book_occur': 8,
        },
    }
    
    rank_order4 = ['a', 'b', 'c']
    learn_order4 = ['b','c','å', 'a']
    char_dict4 = {
        'a': {
            'comps': ['å'],
            'book_occur': 10000,
        },
        'b': {
            'comps': [],
            'book_occur': 1000,
        },
        'c': {
            'comps': [],
            'book_occur': 80,
        },
        'å': {
            'comps': ['ä'],
            'book_occur': 4,
        },
        'ä': {
            'comps': [],
            'book_occur': 2,
        },
    }
   
    def test_skipping(self):
        queue = init_queue(self.rank_order)
        result = prioritize_learn_order(queue, self.char_dict)
        self.assertListEqual(self.learn_order, result)
        
    def test_learning(self):
        queue = init_queue(self.rank_order)
        result = prioritize_learn_order(queue, self.char_dict2)
        self.assertListEqual(self.learn_order2, result)
        
    def test_multiple_comps_and_comp_order(self):
        queue = init_queue(self.rank_order3)
        result = prioritize_learn_order(queue, self.char_dict3)
        self.assertListEqual(self.learn_order3, result)


