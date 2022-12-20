from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.parent
REPO_FONTS = REPO_ROOT / "fonts"
REPO_DIST = REPO_ROOT / "dist"


class SourceSet:
    gen_ei_mono_go: str
    jetbrains_mono: str

    def __init__(self, g: str, j: str):
        self.gen_ei_mono_go = g
        self.jetbrains_mono = j

    def gemg_path(self) -> str:
        return str(REPO_FONTS / "gen-ei-mono-go" / self.gen_ei_mono_go)

    def jbm_path(self) -> str:
        return str(REPO_FONTS / "jetbrains-mono" / self.jetbrains_mono)


class Metadata:
    weight: str
    version: str

    def __init__(self, w: str, v: str):
        self.weight = w
        self.version = v

    def generate_sfnt_names(self):
        japanese_strids = ["Preferred Family", "Preferred Styles"]
        sfnt_dict = {
            "Copyright": "\n".join([
                "Momiage Mono: (C) 2022 kb10uy",
                "",
                "GenEi Mono Gothic: (C) 2020 おたもん",
                "JetBrains Mono: (C) 2020 The JetBrains Mono Project.",
                "Nerd Font: (C) 2014 Ryan L McIntyre.",
            ]),
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
