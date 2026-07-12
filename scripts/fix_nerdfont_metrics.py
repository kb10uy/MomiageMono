"""Align a Nerd Font-patched TTF back to its base font's metrics.

The Nerd Fonts font-patcher (>= 3.x) treats Momiage Mono as a single-width
monospace font: it samples only Latin glyphs (all half-width), so it

  * forces the OS/2 Panose 'Proportion' to Monospaced (9), and
  * enlarges the vertical metrics (win/hhea/typo ascent & descent) plus sets
    the USE_TYPO_METRICS flag to make room for tall icons.

Momiage Mono is actually a dual-width font (half-width Latin + full-width CJK).
The Monospaced flag makes some renderers (e.g. the JetBrains editor on Windows)
lay every glyph in one wide cell, and the enlarged vertical metrics make the
patched font render slightly larger/taller than the base font.

This script copies the width/vertical metrics that matter back from the base
font, so the Nerd Font variant behaves identically to the base font (matching
what the historical releases shipped).

Usage: python3 fix_nerdfont_metrics.py <base.ttf> <nerdfont.ttf>
"""

import sys
from fontTools.ttLib import TTFont


def align_metrics(base_path: str, nf_path: str) -> None:
    base = TTFont(base_path)
    nf = TTFont(nf_path)

    bo, bh = base["OS/2"], base["hhea"]
    no, nh = nf["OS/2"], nf["hhea"]

    # Width classification (undo force_panose_monospaced)
    no.panose.bProportion = bo.panose.bProportion

    # Vertical metrics
    no.sTypoAscender = bo.sTypoAscender
    no.sTypoDescender = bo.sTypoDescender
    no.sTypoLineGap = bo.sTypoLineGap
    no.usWinAscent = bo.usWinAscent
    no.usWinDescent = bo.usWinDescent
    nh.ascent = bh.ascent
    nh.descent = bh.descent
    nh.lineGap = bh.lineGap

    # USE_TYPO_METRICS (fsSelection bit 7) to match the base
    if bo.fsSelection & 0x80:
        no.fsSelection |= 0x80
    else:
        no.fsSelection &= ~0x80

    nf.save(nf_path)
    print(
        f"==> Aligned {nf_path} to base metrics "
        f"(panose={no.panose.bProportion}, win={no.usWinAscent}/{no.usWinDescent}, "
        f"hhea={nh.ascent}/{nh.descent}/{nh.lineGap}, use_typo={bool(no.fsSelection & 0x80)})"
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 fix_nerdfont_metrics.py <base.ttf> <nerdfont.ttf>", file=sys.stderr)
        sys.exit(1)
    align_metrics(sys.argv[1], sys.argv[2])
