from typing import Any
from datetime import date
from pathlib import Path
from .data import SourceSet
from .font import Metadata, fetch_glyph_names, create_insufficient_slots, set_metrics, set_info, generate_mark_tuple, copy_glyphs
import fontforge
import psMat


VERSION = f"1.0-{date.today()}"
SOURCE_SETS = {
    "Regular": SourceSet(
        "MPLUS2-Regular.ttf",
        "SourceHanSans-Regular.otf",
        "JetBrainsMono-Regular.ttf"
    ),
    "Bold": SourceSet(
        "MPLUS2-Bold.ttf",
        "SourceHanSans-Bold.otf",
        "JetBrainsMono-Bold.ttf"
    ),
}


def generate_momiage_mono(source_set: SourceSet, metadata: Metadata, filename: str):
    # Momiage Mono: Prepare
    font = fontforge.font()
    font.encoding = "UnicodeFull"
    set_metrics(font)

    # Momiage Mono: Add Anchor Class
    font.addLookup("marks", "gpos_mark2base", None, generate_mark_tuple())
    font.addLookupSubtable("marks", "anchors")
    font.addAnchorClass("anchors", "Anchor-0")
    font.addAnchorClass("anchors", "Anchor-1")
    font.addAnchorClass("anchors", "Anchor-2")

    # M PLUS 2: Prepare
    font_mp2 = fontforge.open(source_set.m_plus_2_path())

    # M PLUS 2: Scale fullwidth glyphs x1.2 and set width to 2456
    transformation = psMat.compose(
        psMat.translate(75, -70),
        psMat.scale(1.05, 1.05),
    )

    font_mp2.selection.none()
    for glyph in font_mp2.glyphs():
        if glyph.width != 1000:
            continue
        glyph.transform(transformation)
        glyph.width = 1200

    # M PLUS 2: Copy fullwidth glyphs to Momiage Mono
    mp2_glyph_names = fetch_glyph_names(font_mp2, lambda g: g.width == 1200)
    create_insufficient_slots(font, mp2_glyph_names)
    copy_glyphs(font, font_mp2, mp2_glyph_names)

    # JetBrains Mono: Prepare
    font_jbm = fontforge.open(source_set.jbm_path())

    # JetBrains Mono: Copy all glyphs to Momiage Mono
    jbm_glyph_names = fetch_glyph_names(font_mp2, None)
    create_insufficient_slots(font, jbm_glyph_names)
    copy_glyphs(font, font_jbm, jbm_glyph_names)

    set_info(font)
    font.generate(filename, "", ("short-post", "PfEd-lookups", "opentype"))


for weight, source_set in SOURCE_SETS.items():
    metadata = Metadata(weight, VERSION)
    target_filename = Path("dist") / f"MomiageMono-{weight}.ttf"
    generate_momiage_mono(source_set, metadata, str(target_filename))
