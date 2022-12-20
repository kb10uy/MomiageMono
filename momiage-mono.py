from typing import Any
from datetime import date
from pathlib import Path
from scripts import font_action
from scripts.data import SourceSet, Metadata, is_japanese
import fontforge
import psMat


VERSION = f"1.0-{date.today()}"
SOURCE_SETS = {
    "Regular": SourceSet(
        "GenEiMonoGothic-Regular.ttf",
        "JetBrainsMono-Regular.ttf"
    ),
    "Bold": SourceSet(
        "GenEiMonoGothic-Bold.ttf",
        "JetBrainsMono-Bold.ttf"
    ),
}


def generate_momiage_mono(source_set: SourceSet, metadata: Metadata, filename: str):
    # Momiage Mono: Prepare
    font = fontforge.font()
    font.encoding = "UnicodeFull"
    font_action.set_metrics(font)

    # GenEi Mono Gothic
    print("Copying glyphs from GenEi Mono Gothic")

    gemg_font = fontforge.open(source_set.gemg_path())
    gemg_font.em = 2048

    transformation = psMat.compose(
        psMat.translate(102, 0),
        psMat.scale(1.1, 1.1),
    )
    gemg_font.selection.all()
    for glyph in gemg_font.selection.byGlyphs:
        width = is_japanese(glyph.unicode)
        if width is None:
            continue

        glyph.transform(transformation)
        if width == "half":
            glyph.width = 1288
        elif width == "full":
            glyph.width = 2456

    gemg_glyph_names = font_action.fetch_glyph_names(
        gemg_font,
        lambda g: is_japanese(g.unicode) is not None
    )
    font_action.create_insufficient_slots(font, gemg_glyph_names)
    font_action.copy_glyphs(font, gemg_font, gemg_glyph_names)

    # JetBrains Mono
    print("Copying glyphs from JetBrains Mono")

    jbm_font = fontforge.open(source_set.jbm_path())
    jbm_font.em = 2048

    font.importLookups(jbm_font, jbm_font.gsub_lookups)
    font.importLookups(jbm_font, jbm_font.gpos_lookups)

    jbm_glyph_names = font_action.fetch_glyph_names(jbm_font, None)
    font_action.create_insufficient_slots(font, jbm_glyph_names)
    font_action.copy_glyphs(font, jbm_font, jbm_glyph_names)

    # Finalize
    font_action.set_info(font, metadata)
    font.generate(filename, "", ("short-post", "PfEd-lookups", "opentype"))
    font.save(f"{filename}.sfd")


for weight, source_set in SOURCE_SETS.items():
    metadata = Metadata(weight, VERSION)
    target_filename = Path("dist") / f"MomiageMono-{weight}.ttf"
    generate_momiage_mono(source_set, metadata, str(target_filename))
