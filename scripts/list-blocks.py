import sys
from mmtool.unicode import unicode_block
import fontforge


font = fontforge.open(sys.argv[1])
base_em = font.em

found_blocks: set[tuple[int, int, str]] = set()
for glyph in font.glyphs():
    if glyph.unicode == -1:
        continue

    codepoint = glyph.unicode
    char = chr(codepoint)
    block = unicode_block(codepoint)
    glyph_width = glyph.width / base_em

    found_blocks.add(block)

print("Unicode Blocks which the Font have:")
for _, _, block in sorted(found_blocks):
    print(block)
