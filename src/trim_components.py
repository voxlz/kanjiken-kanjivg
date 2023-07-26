def trim_components(char_dict: dict):
    ''' Remove components that are not needed and make tree more shallow.
    
    Components are needed if:
    1. They are a joyo kanji
    2. They are a stroke
    3. They they keep down components of joyo kanji under 6
    4. Used as a radical more than 3 times
    '''
    b = char_dict.items()
    # sort based on affected characters + depth
    b = sorted(b, key=lambda x:  len(x[1]['parent']) + x[1]['depth'] / 10)
    b = filter(lambda x: x[1]['general']['group'] not in ['joyo', 'stroke'], b)
    least_used_radicals = list(b) # can't remove strokes

    # Remove radicals that are not needed -- Todo: Ensure that 习 is removed.
    removable_radicals = set()
    for char in least_used_radicals:

        couldRemove = True
        result = []

        # Check if removing the radical would make the kanji have more than 6 components

        for parent in char[1]['parent']:
            comps: list = char_dict[parent]['comps'].copy()
            while char[0] in comps:
                idx = comps.index(char[0])
                comps[idx:idx+1] = char[1]['comps']

            assert comps != char_dict[parent]['comps'], "Comps should have changed"


            # comps = simplify_comp_list(reduce_comps(comps, parent, char[0]))

            if len(comps) > 4:
                couldRemove = False
                break
            else:
                result.append({parent: (char_dict[parent]['comps'], comps)})

        if couldRemove:
            removable_radicals.add(char[0])
            print(f"radical: {char[0]}")
            for res in result:
                print(res)

                # char_dict.pop(char[0])            

    print(f"Removing {removable_radicals} could be benenfinal")