from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
REPO_FONTS = REPO_ROOT / "fonts"

JAPANESE_CODEPOINT_RANGES: list[tuple[int, int, str]] = [
    # Hiragana
    (0x3041, 0x309F, "full"),

    # Katakana
    (0x30A1, 0x30FF, "full"),
    (0xFF61, 0xFF9F, "half"),

    # Kanji
    (0x4E00, 0x9FFF, "full"),
    (0x2E80, 0x2EFF, "full"),
    (0x3400, 0x4DBF, "full"),
    (0xF900, 0xFAFF, "full"),
    (0x020000, 0x02FA1F, "full"),
    (0x3005, 0x3007, "full"),

    # Punctuations
    (0x3000, 0x303F, "full"),

    # Fullwidth ASCII
    (0xFF00, 0xFF5E, "full"),
    (0xFFE0, 0xFFE6, "full"),
]


class SourceSet:
    gen_ei_mono_go: str
    jetbrains_mono: str

    def __init__(self, g: str, j: str):
        self.gen_ei_mono_go = g
        self.jetbrains_mono = j

    def gemg_path(self) -> str:
        return str(Path("./fonts/gen-ei-mono-go") / self.gen_ei_mono_go)

    def jbm_path(self) -> str:
        return str(Path("./fonts/jetbrains-mono") / self.jetbrains_mono)


class Metadata:
    weight: str
    version: str

    def __init__(self, w: str, v: str):
        self.weight = w
        self.version = v

    def generate_sfnt_names(self):
        japanese_strids = ["Preferred Family", "Preferred Styles"]
        sfnt_dict = {
            "Copyright": "\n".join[
                "Momiage Mono: (C) 2022 kb10uy",
                "",
                "GenEi Mono Gothic: (C) 2020 おたもん",
                "JetBrains Mono: (C) 2020 The JetBrains Mono Project."
            ],
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


def is_japanese(codepoint: int) -> str | None:
    if codepoint == -1:
        return None

    for start, end, width in JAPANESE_CODEPOINT_RANGES:
        if start <= codepoint and codepoint <= end:
            return width

    return None
