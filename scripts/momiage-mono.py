#!/usr/bin/env fontforge -lang=py -script

from os import path
from typing import Any
import fontforge

MPLUS2_DIR = "./fonts/mplus2"
SOURCE_HAN_SANS_DIR = "./fonts/source-han-sans"
JETBRAINS_MONO_DIR = "./fonts/jetbrains-mono"
IGNORE_GLYPH = [
    "uniFEFF",
    ".notdef",
    "m_p_l_u_s_f_o_n_t_s",
]


class Metadata:
    weight: str
    version: str

    def __init__(self, w: str, v: str):
        self.weight = w
        self.version = v


class SourceSet:
    mplus2: str
    source_han_sans: str
    jetbrains_mono: str

    def __init__(self, m: str, s: str, j: str):
        self.mplus2 = m
        self.source_han_sans = s
        self.jetbrains_mono = j

    def mplus2_path(self) -> str:
        return path.join(MPLUS2_DIR, self.mplus2)

    def shs_path(self) -> str:
        return path.join(SOURCE_HAN_SANS_DIR, self.source_han_sans)

    def jbm_path(self) -> str:
        return path.join(JETBRAINS_MONO_DIR, self.jetbrains_mono)


def generate_momiage_mono(source_set: SourceSet, metadata: Metadata, filename: str):
    print(f"=> Generating Weight {weight}")

    font_jbm = fontforge.open(source_set.jbm_path())
    font_jbm.em = 2048

    font_jbm.mergeFonts(source_set.mplus2_path())
    # font_jbm.mergeFonts(source_set.shs_path())

    # font_shs = fontforge.open(source_set.shs_path())
    # font_mplus2 = fontforge.open(source_set.mplus2_path())

    # Remove duplicate glyphs
    # exclude_glyphs(font_jbm, font_shs)
    # exclude_glyphs(font_jbm, font_mplus2)
    # exclude_glyphs(font_mplus2, font_shs)

    # font_shs.mergeFonts(source_set.mplus2_path())
    # font_shs.mergeFonts(source_set.jbm_path())

    # Merge fonts into JetBrains Mono
    # paste_glyphs(font_jbm, font_mplus2)
    # paste_glyphs(font_jbm, font_shs)

    # Set metadata
    font_jbm.os2_vendor = "n935"
    font_jbm.sfnt_names = generate_sfnt_names(metadata)
    font_jbm.gasp = generate_gasp()

    # Generate
    font_jbm.generate(filename, "", ("short-post", "PfEd-lookups", "opentype"))


def exclude_glyphs(font_needle: Any, font_haystack: Any):
    print(f"==> Excluding Glyphs of {font_needle.familyname} from {font_haystack.familyname}")

    font_needle.selection.all()
    font_haystack.selection.none()

    for glyph in font_needle.selection.byGlyphs:
        if glyph.glyphname in font_haystack and not glyph_should_be_ignored(glyph):
            font_haystack.selection.select(("more",), glyph.glyphname)
    font_haystack.clear()


def paste_glyphs(font_dest: Any, font_src: Any):
    print(f"==> Copying Glyphs to {font_dest.familyname} from {font_src.familyname}")

    font_dest.selection.none()
    font_src.selection.none()
    for glyph in font_src.glyphs():
        if glyph_should_be_ignored(glyph):
            continue
        print(glyph.glyphname)
        font_src.selection.select(glyph.glyphname)
        font_src.copy()
        font_dest.selection.select(glyph.glyphname)
        font_dest.paste()


def glyph_should_be_ignored(glyph: Any):
    if glyph.glyphname in IGNORE_GLYPH:
        return True
    return False


def generate_sfnt_names(metadata: Metadata) -> tuple:
    japanese_strids = ["Preferred Family", "Preferred Styles"]
    sfnt_dict = {
        "Copyright": """\
            Momiage Mono

            M PLUS 2: (C) 2021 The M+ FONTS Project.
            Source Han Sans: (C) 2014-2021 Adobe.
            JetBrains Mono: (C) 2020 The JetBrains Mono Project.""",
        "Vendor URL": "https://github.com/kb10uy/MomiageMono",
        "Version": metadata.version,
        "Preferred Family": "Momiage Mono",
        "Preferred Styles": metadata.weight,
        "Family": f"Momiage Mono {metadata.weight}",
        "SubFamily": metadata.weight,
        "Fullname": f"MomiageMono-{metadata.weight}",
        "PostScriptName": f"MomiageMono-{metadata.weight}",
    }

    sfnt_names = []
    for strid, value in sfnt_dict.items():
        sfnt_names.append(("English (US)", strid, value))
    for strid in japanese_strids:
        sfnt_names.append(("Japanese", strid, sfnt_dict[strid]))

    return tuple(sfnt_names)


def generate_gasp() -> tuple:
    return (
        (8, ("antialias",)),
        (13, ("antialias", "symmetric-smoothing")),
        (65535, ("antialias", "symmetric-smoothing")),
    )


VERSION = "1.0"
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

for weight, source_set in SOURCE_SETS.items():
    metadata = Metadata(weight, VERSION)
    target_filename = path.join("dist", f"MomiageMono-{weight}.ttf")
    generate_momiage_mono(source_set, metadata, target_filename)
