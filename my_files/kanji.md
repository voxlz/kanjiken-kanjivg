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

## The KanjiKen System - Principles

Let's talk about some principles I'm going for here.

1. **No duplicates**. If there are any characters that look identical but are not, so called homoglyphs,  they should be considered identical. (Ex. ㇁ == ㇓)
2. **No variations**. For two components to be considered identical, they need to have matching stroke type, stroke order, and stroke propotions. (Ex. ⺅ !=  人 | ⼇ != 丄)
3. **Max 6 components**. Every character is broken down to 2-6 components, ideally 4. This is a good compromise between complexity and usability.
4. **Keep stroke order**. Components that contain non consecutive strokes, i.e. pausing the component to draw something else,  are not allowed. (Ex. 口 and 戈)
5. **Prune components**. If a component can be removed without breaking any above rule, and it does not push component count beyond 4  elsewhere, it should be.
6. **Consistency**. A character should always be represented by the same components. Inconsistencies are not allowed, due to the induced complexity.
7. **Shallowness**. Certain components with 3 strokes can be broken down into 2 components. To avoid unnessesary depth, this is not allowed. (Ex. 士 != [十 + 一])

These rules ensure that knowing the components of a characters is knowing how to draw the character. That is the goal of the KanjiKen system.

## The KanjiKen Order

Which order you should learn the characters in depends on the learner.

1. Never learn a character before you know all its components.
2. Prioritize learning characters that are more common.

Should you learn 番 or 万 first?

番 =  ['⾤', '田']
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

| Radical | Code | Name | N-comps | Derivative |
| -- | -- | -- | -- | -- |
| ⿖ | 2FD6 | amongus | 4 |   薦,  鹿
| ⿗ | 2FD7 | kobold | 5 | 龍
| ⿘ | 2FD8 | torch | 3 |  減, 幾, 歳, etc.
| ⿙ | 2FD9 | bridge | 2 |  皿
| ⿚ | 2FDA | table-flip| 3 | 皿

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
