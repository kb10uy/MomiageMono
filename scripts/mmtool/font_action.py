from collections.abc import Callable
from functools import reduce
from .data import Target
import fontforge
import psMat


def compose_transforms(transforms: list[tuple]) -> tuple:
    return reduce(
        lambda composed, next: psMat.compose(next, composed),
        transforms,
        psMat.identity()
    )


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
    new_slots = 0
    for glyph_name in glyph_names:
        if font.findEncodingSlot(glyph_name) == -1:
            font.createChar(-1, glyph_name)
            new_slots += 1

    print(f"==> Created {new_slots} new slots")


def copy_glyphs(dest: fontforge.font, src: fontforge.font, glyph_names: list[str]):
    for i, glyph_name in enumerate(glyph_names):
        if i % 500 == 0:
            print(f"==> Copied {i} glyphs")

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
    font.os2_winascent = 1100
    font.os2_windescent = 200
    font.os2_typoascent = 800
    font.os2_typodescent = -200
    font.hhea_ascent = 1100
    font.hhea_descent = -200
    font.em = 2048


def set_info(font: fontforge.font, target: Target):
    target_style = target.style()

    font.fontname = f"MomiageMono-{target_style.subfamily_id()}"
    font.familyname = f"Momiage Mono"
    font.weight = target_style.weight_name()
    font.italicangle = -9 if target_style.is_italic() else 0
    font.os2_weight = target_style.weight_value()
    font.gasp_version = 1
    font.gasp = _generate_gasp()
    font.sfnt_names = _generate_sfnt_names(target)


def _generate_gasp() -> tuple:
    return (
        (8, ("antialias",)),
        (13, ("antialias", "symmetric-smoothing")),
        (65535, ("antialias", "symmetric-smoothing")),
    )


def _generate_sfnt_names(target: Target) -> tuple:
    subfamily_name = target._style.subfamily_name()
    subfamily_id = target._style.subfamily_id()

    sfnt_dict = {
        "Copyright": "\n".join([
            "Momiage Mono: (C) 2022 kb10uy",
            "",
            "GenEi Mono Gothic: (C) 2020 おたもん",
            "JetBrains Mono: (C) 2020 The JetBrains Mono Project.",
            "Nerd Font: (C) 2014 Ryan L McIntyre.",
        ]),
        "Family": f"Momiage Mono",
        "SubFamily": subfamily_name,
        "UniqueID": f"{target.version()};MomiageMono-{subfamily_id}",
        "Fullname": f"Momiage Mono {subfamily_name}",
        "Version": target.version(),
        "Vendor URL": "https://github.com/kb10uy/MomiageMono",
    }

    sfnt_names = []
    for strid, value in sfnt_dict.items():
        sfnt_names.append(("English (US)", strid, value))

    return tuple(sfnt_names)
