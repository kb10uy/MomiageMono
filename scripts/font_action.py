from collections.abc import Callable
from .data import Metadata
import fontforge


def fetch_glyph_names(font: fontforge.font, predicate: Callable[[fontforge.glyph], bool] | None) -> list[str]:
    glyph_names = []

    # font.glyphs() would cause SEGV
    font.selection.all()
    for glyph in font.selection.byGlyphs:
        if predicate is not None and not predicate(glyph):
            continue
        glyph_names.append(glyph.glyphname)
    font.selection.none()

    return glyph_names


def create_insufficient_slots(font: fontforge.font, glyph_names: list[str]):
    for glyph_name in glyph_names:
        if font.findEncodingSlot(glyph_name) == -1:
            font.createChar(-1, glyph_name)


def copy_glyphs(dest: fontforge.font, src: fontforge.font, glyph_names: list[str]):
    for i, glyph_name in enumerate(glyph_names):
        if i % 100 == 0:
            print(f"=> Copied {i} glyphs")
        src.selection.select(glyph_name)
        src.copy()
        dest.selection.select(glyph_name)
        dest.paste()


def set_metrics(font: fontforge.font):
    font.ascent = 800
    font.descent = 200
    font.os2_version = 4
    font.os2_use_typo_metrics = False
    font.os2_winascent_add = False
    font.os2_windescent_add = False
    font.os2_typoascent_add = False
    font.os2_typodescent_add = False
    font.hhea_ascent_add = False
    font.hhea_descent_add = False
    font.os2_winascent = 1000
    font.os2_windescent = 200
    font.os2_typoascent = 800
    font.os2_typodescent = -200
    font.hhea_ascent = 1000
    font.hhea_descent = -200
    font.em = 2048


def set_info(font: fontforge.font, metadata: Metadata):
    font.os2_vendor = "n935"
    font.sfnt_names = metadata.generate_sfnt_names()
    font.gasp_version = 1
    font.gasp = _generate_gasp()


def _generate_gasp() -> tuple:
    return (
        (8, ("antialias",)),
        (13, ("antialias", "symmetric-smoothing")),
        (65535, ("antialias", "symmetric-smoothing")),
    )
