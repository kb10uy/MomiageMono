from collections.abc import Callable
from .data import Metadata
import fontforge


class Metadata:
    weight: str
    version: str

    def __init__(self, w: str, v: str):
        self.weight = w
        self.version = v

    def generate_sfnt_names(self):
        japanese_strids = ["Preferred Family", "Preferred Styles"]
        sfnt_dict = {
            "Copyright": """\
                Momiage Mono

                M PLUS 2: (C) 2021 The M+ FONTS Project.
                Source Han Sans: (C) 2014-2021 Adobe.
                JetBrains Mono: (C) 2020 The JetBrains Mono Project.""",
            "Vendor URL": "https://github.com/kb10uy/MomiageMono",
            "Version": self.version,
            "Preferred Family": "Momiage Mono",
            "Preferred Styles": self.weight,
            "Family": f"Momiage Mono {self.weight}",
            "SubFamily": self.weight,
            "Fullname": f"MomiageMono-{self.weight}",
            "PostScriptName": f"MomiageMono-{self.weight}",
        }

        sfnt_names = []
        for strid, value in sfnt_dict.items():
            sfnt_names.append(("English (US)", strid, value))
        for strid in japanese_strids:
            sfnt_names.append(("Japanese", strid, sfnt_dict[strid]))

        return tuple(sfnt_names)


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
    for glyph_name in glyph_names:
        src.selection.select(glyph_name)
        src.copy()
        dest.selection.select(glyph_name)
        src.paste()


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


def generate_mark_tuple() -> tuple:
    feature = "mark"
    languages = tuple([
        ("DFLT", "dflt"),
        ("latn", "dflt"),
    ])
    return tuple([
        (feature, languages),
    ])
