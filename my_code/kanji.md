# Kanji definitions

## Naming convention

To have a consistent variable naming convention, I will now break down and myself define different types of japanese characters.

| Name | Example | Description |
| --- | --- | ----------- |
| Compounds | 複合語 | Words made up of multiple kanji
| Kanji | 漢, 字 | Defined as words in a dictionary
| Contractions | 駦 | Neither kanji nor radical. Often made from two other kanji. May not be used in japanese.
| Radicals | 亻, 𠂉 | A group of 2-5 strokes that occur as component in kanji.
| Strokes | ㇒, ㇑ | A single brush stroke.
| Part / Component | ㇒, 字 | Part of another kanji, can be any of the above

## Kanji History

1946: JGov announced touyou kanji list (1,850 characters, 当用漢字表 = present use kanji list, introduced Shinjitai (new character forms))
1981: JGov announced jouyou kanji list (1,945 characters, 常用漢字表 = daily use kanji list)
2010: JGov updated   jouyou kanji list (2,136 characters)

## Principles

Let's talk about some principles I'm going for here.

1. **No duplicates**. If there are any characters that look identical to each other(homoglyphs),  they should be considered identical. Learning the sun radical vs the sun kanji separably, for example, is a waste of time. Note: They have to have the correct strokes and order to be identical! Kanji and strokes are preferred over radicals.
2. **6 components or less**. I want the user to be able to quickly input a kanji, so I will limit myself to 6 components or less. This is a bit arbitrary, but I think it's a good compromise between complexity and usability. This may force me to invent new radicals, but that's fine.
3. **Keep proper stroke order**. Learning kanji means learning proper stroke order. Therefore I will not allow radicals that contain non consecutive strokes. '戈' for example, where the first line is sometimes drawn before pausing and drawing other stuff, to later finish the radical.
4. **Keep it simple**. Unnecessary complexity should be avoided. If a radical is only used in one or two kanji, and I can make due without it (it won't increase components beyond 6 elsewhere), I will. This is to keep the number of radicals and additional kanjis down to a minimum, and to keep the system simple.
5. **Consistency**. The same kanji should always be represented by the same components. I won't allow inconsistencies, as these lead to confusion and mistakes for new learners.

## Unicode blocks

* Kangxi radicals: 2F00–2FD5
* CJK radicals supplement: 2E80–2EFF
* CJK Strokes: 31C0–31EF (31C0-31E3 used)

## Notes

### Avoid mismatch strokes and unicode representations

Variants and Original characters. If it's a variant but has no original character, that means there is no proper unicode representation of the component, which is undesirable. Like 滕 with the top strokes leaning inward like 𣳾.

## Radicals

### Drawn Radical simplification

Some radicals are written differently from their unicode representation. Ex. 人, 八, 入 are all written with two sloped strokes, but the unicode representation is different.

### Custom radicals

I have invented new radicals. This was due to not finding a good reduction of strokes with the available unicode characters.

* ⿖ (amongus,  4 comps) : part of  薦,  鹿
* ⿗ (drag-on,  5 comps) : part of 龍
* ⿘ (torch,       3 comps) : part of 減, 幾, 歳, etc.
* ⿙ (bridge,     2 comps) : part of 皿
* ⿚ (??, 3 comps) : part of 皿

### Positional radicals

Certain radicals have multiple representations. Here follows a list of radical pars not considered homoglyphs, and if I consider them identical or not.

#### Scaled versions

These look identical and will be considered the same. (Fullsize character will be used)

* 皿 | ⺲
* 𠂊 | ⺈
* 人 | 𠆢
* 丄 | ⼇ (not joyo)
* 卄 | 艹 (not joyo)

#### Different strokes / stroke order

These may come from a kanji, but look different / have different stroke order. They will be considered different.

* 人 | ⺅

#### Weird radicals

* ?   | 龶  There does not seem to be a fullsize version of this positional...
* 耒  is a radical but all joyo kanji that use it have a straight line at the top.
* 竹 | 𥫗 ?

#### Written vs Unicode

To make matters worse, some characters are written differently from how they are precented in unicode. This is the case for 人, 八, 入, and possibly more. I will use the hand written strokes of these characters, since stroke order only matters when writing by hand, and we already care about that.

### Shiny (shinjitai) kanji

Kanji where joyo is using old radical / version of kanji compared to shinjitai (extended).

* 籠 Jōyō -> 篭 shinjitai亠 
