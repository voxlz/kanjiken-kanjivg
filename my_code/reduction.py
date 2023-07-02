
reduction_rules = [
    # ('一*', '一'), # 一* => 一 simplifies rules
    # ('㇑*', '㇑*'), # 一* => 一 simplifies rules
    ('一,巾','帀'),
    ('㇒,㇙,㇒,㇏', '𧘇'),
    ('㇑,㇑,㇔,㇒,一', '业'),
    ('㇑,㇑,丶,㇒,㇀', '业'),
    ('㇑,㇑,丶,㇒,一', '业'),
    ('㇕,一,一', '彐'),
    ('一,㇑,㇑,㇑,㇑', '卌'),
    ('一,㇑,㇑,㇑', '卅'),
    ('一,㇑,㇑,一,一', '𠀎'),
    ('一,㇑,㇑', '卄'),
    ('一,一,一', '三'),
    ('㇑,㇑,一', 'ᚇ'), # if this is problematic, Check for starting with ㇕
    ('一,一', '二'),
    ('㇒,㇑,㇒,㇔', '𧘇'),
    ('㇑,㇕,一,㇕,一', '㠯'),
    ('㇑,㇕,㇔', '卪'),
    ('㇔,㇒', '丷'),
    ('人,一,口,人', '㑒'),
    ('㇑,㇕', '⨅'),
    ('㇒,㇔', '八'),
    ('㇒,㇚', '刂'),
    ('三,㇑', '龶'),
    ('人,人,人,人', '𠈌'),
    ('㇆,㇔,㇀', '习'),
    ('㇕,一', 'コ'),
    ('一,㇑', '十'),
    
    # Questionable rules
    ('丿,丶', '冫'), # Technically correct, could lead to more issues down the line...
    
    # Probably bad rules
    ('㇂,丿,丶', '义'), # Missing hook, not a huge fan of this one.
    ('㇂,㇒,㇔', '义'), # Missing hook, not a huge fan of this one.
    ('㇒,㇏', '人'), 
    # ('艹', '卄'), # They look the same :D
    # ('𠆢', '人'), 
    # ('⺈', '𠂊')   
]


def get_rules():
    return reduction_rules