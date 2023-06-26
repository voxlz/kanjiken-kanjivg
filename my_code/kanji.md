# Kanji definitions

To have a consistent variable naming convention, I will now break down and define different types of japanese characters.

| Name | Example | Description |
| --- | --- | ----------- |
| Compounds | 複合語 | Words made up of multiple kanji
| Kanji | 漢, 字 | Defined as words in a dictionary
| Contractions | 駦 | Neither kanji nor radical. Often made from two other kanji. May not be used in japanese.
| Radicals | 亻, 𠂉 | A group of strokes in kanji.
| Strokes | ㇒, ㇑ | A single stroke / line in a kanji.
| Part / Component | ㇒, 字 | Part of another kanji, can be any of the above

Let's talk about some principles I'm going for here.

1. No duplicates. If there are radicals that look identical, are homoglyphs or scaled version of kanji, or radicals that overlap with kanji, they should be considered identical. Learning the sun radical vs the sun kanji separably, for example, is a waste of time.
2. 6 components or less. I want the user to be able to quickly input a kanji, so I will limit myself to 6 components or less. This is a bit arbitrary, but I think it's a good compromise between complexity and usability. This may force me to invent new radicals, but that's fine.
3. Keep proper stroke order. Component input should be done in order. I find it ineffective to learn kanji without proper stroke order. This means that certain "proper" radicals components will be excluded, since they are not drawn in one go. '戈' in for example, where the first line is sometimes drawn before pausing and drawing other stuff, to later finish the radical. This would be 2 components in my system.
4. Keep it simple. Unnessesary complexity should be avoided. If a radical is only used in one or two kanji, and I can make due without it (it won't increase components beyond 6 elsewhere), I will. This is to keep the number of radicals and additional kanjis down to a minimum, and to keep the system simple.
