from datetime import date
from pathlib import Path
from mmtool import font_action
from mmtool.data import SourceSet, Metadata, is_japanese, REPO_DIST
from mmtool.unicode import block_width_of, unicode_block_of, target_width_of
import fontforge
import psMat

GENEI_UNIFORM_TRANSFORM = psMat.compose(
    psMat.translate(102, 0),
    psMat.scale(1.1, 1.1)
)
GENEI_F2H_TRANSFORM = psMat.compose(
    psMat.translate(-205, 0),
    psMat.scale(0.8, 0.8)
)
GENEI_H2F_TRANSFORM = psMat.compose(
    psMat.translate(589, 0),
    psMat.scale(1.25, 1.25)
)

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


def _copy_genei_mono_gothic(font: fontforge.font, source_set: SourceSet):
    gemg_font = fontforge.open(source_set.gemg_path())
    gemg_font.em = 2048

    gemg_font.selection.all()
    gemg_glyph_names = []
    for glyph in gemg_font.selection.byGlyphs:
        if glyph.unicode == -1:
            continue

        block = unicode_block_of(glyph.unicode)
        block_info = block_width_of(block[2])
        if block_info is None:
            continue

        block_font_tag = block_info[1]
        if block_font_tag is not None and block_font_tag != "gemg":
            continue

        # TODO: deal with zero-width glyph
        glyph_width = "full" if glyph.width / 2048 > 0.95 else "half"
        target_width = target_width_of(glyph.unicode)

        if glyph_width == target_width:
            glyph.transform(GENEI_UNIFORM_TRANSFORM)
        elif glyph_width == "full":
            print(f"Applying full-to-half transform for U+{glyph.unicode:06X}")
            glyph.transform(GENEI_F2H_TRANSFORM)
        elif glyph_width == "half":
            print(f"Applying half-to-full transform for U+{glyph.unicode:06X}")
            glyph.transform(GENEI_H2F_TRANSFORM)
        glyph.width = 2456 if target_width == "full" else 1228

        gemg_glyph_names.append(glyph.glyphname)

    font_action.create_insufficient_slots(font, gemg_glyph_names)
    font_action.copy_glyphs(font, gemg_font, gemg_glyph_names)


def _copy_jetbrains_mono(font: fontforge.font, source_set: SourceSet):
    jbm_font = fontforge.open(source_set.jbm_path())
    jbm_font.em = 2048

    font.importLookups(jbm_font, jbm_font.gsub_lookups)
    font.importLookups(jbm_font, jbm_font.gpos_lookups)

    jbm_glyph_names = font_action.fetch_glyph_names(jbm_font, None)
    font_action.create_insufficient_slots(font, jbm_glyph_names)
    font_action.copy_glyphs(font, jbm_font, jbm_glyph_names)


def generate_momiage_mono(source_set: SourceSet, metadata: Metadata, filename: Path):
    # Momiage Mono
    font = fontforge.font()
    font.encoding = "UnicodeFull"
    font_action.set_metrics(font)

    # GenEi Mono Gothic
    print("Copying glyphs from GenEi Mono Gothic")
    _copy_genei_mono_gothic(font, source_set)

    # JetBrains Mono
    print("Copying glyphs from JetBrains Mono")
    _copy_jetbrains_mono(font, source_set)

    # Finalize
    font_action.set_info(font, metadata)
    font.generate(
        str(filename),
        "",
        ("short-post", "PfEd-lookups", "opentype")
    )


for weight, source_set in SOURCE_SETS.items():
    metadata = Metadata(weight, VERSION)
    target_filename = REPO_DIST / f"MomiageMono-{weight}.ttf"
    generate_momiage_mono(source_set, metadata, target_filename)
