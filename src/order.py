# Attempt prioritizing kanji
import csv
from  queue import LifoQueue
from sortedcollections import OrderedSet

from src.radicals import get_strokes

def get_sorted_joyo_frequencies(char_dict, fileName="book_characters.csv"):
    ''' Get the frequency and rank of each written character. Returns a list of dictionaries. '''
    
    with open(f"data/scriptin-kanji-frequency/{fileName}", "r", encoding="utf8") as mapping:
        reader = csv.reader(mapping, delimiter=",")
        next(reader) # Skip header

        kanji_ranked = []
        total_chars = 0

        for row in reader:
            rank, code, char, char_count = row
            if char in char_dict:
                total_chars += int(char_count)
                medium = fileName.split("_")[0]
                update = {f'{medium}_rank': len(kanji_ranked), f'{medium}_occur': char_count}
                kanji_ranked.append(char)
                char_dict[char] |= update
    
    return kanji_ranked, total_chars

def find_not_learned_comps(char, learned, char_dict, strokes):
    ''' Recursively get all components that are not learned yet. Ensure no duplicates, and that child components are ordered **BEFORE** their parents. '''
    
    comps = {c for c in char_dict[char]['comps'] if c not in strokes}
    not_learned = {c for c in comps if c not in learned}
    not_learned = OrderedSet(sorted(not_learned, key=lambda c: char_dict[c]['book_occur'], reverse=True))
    for c in not_learned:
        not_learned = find_not_learned_comps(c, learned, char_dict, strokes) | not_learned
    return not_learned

# for char in joyo:
#     if 'rank' not in char_dict[char]:
#         print(f"Character {char} is not in the kanji frequency list")
#         update = {'char': char, 'rank': len(kanji_ranked), 'char_count': char_count}
#         char_dict[char] |= update
#         kanji_ranked.append( update)

# avg_char_count = total_chars / len(joyo)
def peak(num, queue):
    return list(reversed(queue.queue[-num:]))

def init_queue(order):
    queue = LifoQueue()
    for char in reversed(order):
        queue.put(char)
    return queue

def prioritize_learn_order(queue: LifoQueue, char_dict):
    ''' Prioritize the learn order. Queue is sorted by frequency.
    Rules:
    1. Maximize frequency score at every step.
    2. Only characters that have all components learned can be learned.
    '''
    learn_order = []
    strokes = get_strokes()
    
    while not queue.empty():
        
        def get_next_char_to_learn():
            ## Get the current character
            curr_char = queue.get()
            
            # Get all direct components that are not strokes.
            non_stroke_comps = [c for c in char_dict[curr_char]['comps'] if c not in strokes]

            # Components are all learned, so learn this character. (Sorted list remember)
            if all(c in learn_order for c in non_stroke_comps):
                learn_order.append(curr_char)
            else:
                # See if  worth learning char's components + char, or if it's better to skip it.
                not_learned = find_not_learned_comps(curr_char, learn_order, char_dict, strokes)
                not_learned = not_learned | [curr_char]

                
                # If skipping possible?
                qsize = queue.qsize()
                if (len(not_learned) <= qsize):
                    gain_learning = get_total_char_count(not_learned, char_dict)
                    next_few_chars = peak(len(not_learned), queue)
                    gain_skipping = get_total_char_count(next_few_chars, char_dict)
                elif (len(not_learned) > qsize and qsize > 0):
                    gain_learning = get_total_char_count(list(not_learned)[:qsize], char_dict)
                    next_few_chars = peak(qsize, queue)
                    gain_skipping = get_total_char_count(next_few_chars, char_dict)
                else:
                    # Skipping is not possible.
                    gain_learning = 1
                    gain_skipping = 0
                
                if (gain_learning >= gain_skipping):

                    # Add not learned components to the top of queue
                    for curr_char in reversed(not_learned):
                        count = char_dict[curr_char]['char_count'] if 'char_count' in char_dict[curr_char] else 0
                        rank = char_dict[curr_char]['rank'] if 'rank' in char_dict[curr_char] else -1
                        queue.put(curr_char)
                else:
                    if (not queue.empty()):
                        get_next_char_to_learn()
                        queue.put(curr_char)
                    else:
                        learn_order.append(curr_char)
        
        get_next_char_to_learn()
    
    return learn_order

def get_total_char_count(list, char_dict):
    return  sum(char_dict[c]['book_occur'] for c in list if 'book_occur' in char_dict[c])

def get_learn_order(char_dict):
    ''' In what order the user should learn the kanji. '''
    kanji_order, total = get_sorted_joyo_frequencies()
    queue = init_queue(kanji_order)
    learn_order = prioritize_learn_order(queue, char_dict)

    print()
    

    
    
