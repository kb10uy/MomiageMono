#!/usr/bin/env fontforge -lang=py -script

from typing import Any
from datetime import date
from pathlib import Path
import fontforge
import psMat


class Metadata:
    weight: str
    version: str

    def __init__(self, w: str, v: str):
        self.weight = w
        self.version = v


class SourceSet:
    m_plus_2: str
    source_han_sans: str
    jetbrains_mono: str

    def __init__(self, m: str, s: str, j: str):
        self.m_plus_2 = m
        self.source_han_sans = s
        self.jetbrains_mono = j

    def m_plus_2_path(self) -> str:
        return str(Path("./fonts/m-plus-2") / self.m_plus_2)

    def shs_path(self) -> str:
        return str(Path("./fonts/source-han-sans") / self.source_han_sans)

    def jbm_path(self) -> str:
        return str(Path("./fonts/jetbrains-mono") / self.jetbrains_mono)


def generate_momiage_mono(source_set: SourceSet, metadata: Metadata, filename: str):
    print(f"=> Generating Weight {weight}")

    # Momiage Mono: Prepare
    font = fontforge.font()
    font.encoding = "UnicodeFull"

    # Momiage Mono: Add Anchor Class
    font.addLookup("marks", "gpos_mark2base", None,
                   generate_mark_feature_tuple())
    font.addLookupSubtable("marks", "anchors")
    font.addAnchorClass("anchors", "Anchor-0")
    font.addAnchorClass("anchors", "Anchor-1")
    font.addAnchorClass("anchors", "Anchor-2")

    # M PLUS 2: Prepare
    font_mp2 = fontforge.open(source_set.m_plus_2_path())

    # M PLUS 2: Scale fullwidth glyphs x1.2 and set width to 2456
    transformation = psMat.compose(
        psMat.translate(0, -100),
        psMat.scale(1.2, 1.2),
    )

    font_mp2.selection.none()
    for fw_glyph in font_mp2.glyphs():
        if fw_glyph.width != 1000:
            continue
        fw_glyph.transform(transformation)
        fw_glyph.width = 1200

    # M PLUS 2: Copy fullwidth glyphs to Momiage Mono
    font.selection.none()
    font_mp2.selection.none()
    for fw_glyph in font_mp2.glyphs():
        if fw_glyph.width != 1200:
            continue

        print(f"Copying {fw_glyph.glyphname} from M PLUS 2")
        # Make sure given glyphname exist
        if font.findEncodingSlot(fw_glyph.glyphname) == -1:
            font.createChar(-1, fw_glyph.glyphname)

        font_mp2.selection.select(fw_glyph)
        font_mp2.copy()
        font.selection.select(fw_glyph.glyphname)
        font.paste()

    # JetBrains Mono: Prepare
    font_jbm = fontforge.open(source_set.jbm_path())

    # JetBrains Mono: Copy all glyphs to Momiage Mono
    font.selection.none()
    font_jbm.selection.none()
    for glyph in font_jbm.glyphs():
        print(f"Copying {glyph.glyphname} from JetBrains Mono")
        # Make sure given glyphname exist
        if font.findEncodingSlot(glyph.glyphname) == -1:
            font.createChar(-1, glyph.glyphname)

        font_jbm.selection.select(glyph)
        font_jbm.copy()
        font.selection.select(glyph.glyphname)
        font.paste()

    fw_glyph = None
    glyph = None
    font_jbm = None
    font_mp2 = None

    # Momiage Mono: Set metadata
    font.os2_vendor = "n935"
    font.sfnt_names = generate_sfnt_names(metadata)
    font.gasp_version = 1
    font.gasp = generate_gasp()
    set_metrics(font)

    # Momiage Mono: Generate
    print(f"Writing {filename}")
    font.generate(filename, "", ("short-post", "PfEd-lookups", "opentype"))


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


def generate_mark_feature_tuple() -> tuple:
    feature = "mark"
    languages = tuple([
        ("DFLT", "dflt"),
        ("latn", "dflt"),
    ])
    return tuple([
        (feature, languages),
    ])


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

for weight, source_set in SOURCE_SETS.items():
    metadata = Metadata(weight, VERSION)
    target_filename = Path("dist") / f"MomiageMono-{weight}.ttf"
    generate_momiage_mono(source_set, metadata, str(target_filename))
