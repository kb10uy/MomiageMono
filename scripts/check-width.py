import sys
from mmtool.unicode import target_width_of, block_width_of, unicode_block_of
import fontforge

font = fontforge.open(sys.argv[1])
font_tag = sys.argv[2]
base_em = font.em

for glyph in font.glyphs():
    if glyph.unicode == -1:
        continue

    codepoint = glyph.unicode
    str_expr = f"U+{codepoint:06X} '{chr(codepoint)}'"
    _, _, block_name = unicode_block_of(codepoint)

    block_width = block_width_of(block_name)
    target_width = target_width_of(codepoint)
    glyph_width = "full" if glyph.width / base_em > 0.95 else "half"

    if block_width is None:
        continue

    if block_width[0] == "complex":
        # print(f"[I] {str_expr} has complex width, skipping")
        continue

    if block_width[1] is not None and block_width[1] != font_tag:
        # print(f"[I] {str_expr} will not be copied, skipping")
        continue

    if not (block_width[0] == target_width and block_width[0] == glyph_width):
        print(f"[E] {str_expr} has different width")
        print(f"    Unicode Block   : {block_width[0]} (from {block_name})")
        print(f"    East Asian Width: {target_width}")
        print(f"    Glyph           : {glyph_width}")
        continue

    # print(f"[I] {str_expr} has consistent width: {block_width}")
