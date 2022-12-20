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

    block_info = block_width_of(block_name)
    target_width = target_width_of(codepoint)
    glyph_width = "full" if glyph.width / base_em > 0.95 else "half"

    if block_info is None:
        continue
    block_width, block_font_tag = block_info

    if block_width == "complex":
        # print(f"[I] {str_expr} has complex width, skipping")
        continue

    if block_font_tag is not None and block_font_tag != font_tag:
        # print(f"[I] {str_expr} will not be copied, skipping")
        continue

    if target_width != glyph_width:
        print(f"[E] {str_expr} has different width")
        print(f"    Unicode Block    : {block_name}")
        print(f"    East Asian Width : {target_width}")
        print(f"    Glyph            : {glyph_width}")
        continue

    # print(f"[I] {str_expr} has consistent width: {block_width}")
