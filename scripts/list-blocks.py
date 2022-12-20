# East Asian Width Checker
# F  (Fullwidth) "FULLWIDTH" chars; ＡＢＣ
# H  (Halfwidth) "HALFWIDTH" chars; ｱｲｳ
# W  (Wide)      Wide chars;        あア漢
# Na (Narrow)    Narrow chars;      ABC
# A  (Ambiguous) Ambiguous chars;   ↑↓←→
# N  (Neutral)   Neutral chars;     Áς

from unicodedata import east_asian_width, category
import sys
from mmtool.unicode import find_block
import fontforge


font = fontforge.open(sys.argv[1])
base_em = font.em

found_blocks: set[tuple[int, int, str]] = set()
for glyph in font.glyphs():
    if glyph.unicode == -1:
        continue

    codepoint = glyph.unicode
    char = chr(codepoint)
    block = find_block(codepoint)
    eaw = east_asian_width(char)
    glyph_width = glyph.width / base_em

    found_blocks.add(block)
    # print(f"U+{codepoint:06X} '{char}' [{eaw}] => {block}")

print("Unicode Blocks which the Font have:")
for _, _, block in sorted(found_blocks):
    print(block)
