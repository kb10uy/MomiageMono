from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.parent
REPO_FONTS = REPO_ROOT / "fonts"
REPO_DIST = REPO_ROOT / "dist"

WEIGHT_VALUES = {
    "Regular": 400,
    "Bold": 700,
}


class Style:
    _weight: str | None
    _italic: bool

    def __init__(self, weight: str | None, italic: bool):
        self._weight = weight
        self._italic = italic

    def weight_name(self) -> str:
        if self._weight is None:
            return "Regular"
        else:
            return self._weight

    def weight_value(self):
        return WEIGHT_VALUES[self.weight_name()]

    def is_italic(self) -> bool:
        return self._italic

    def subfamily_name(self) -> str:
        name = "Italic" if self._italic else ""
        if self._weight is not None:
            name = f"{self._weight} {name}"
        if name == "":
            name = "Regular"
        return name

    def subfamily_id(self) -> str:
        return self.subfamily_name().replace(" ", "")


class Target:
    _version: str
    _style: Style
    _gen_ei_mono_go: str
    _jetbrains_mono: str

    def __init__(self, version: str, style: Style, g: str, j: str):
        self._version = version
        self._style = style
        self._gen_ei_mono_go = g
        self._jetbrains_mono = j

    def version(self) -> str:
        return self._version

    def style(self) -> Style:
        return self._style

    def gemg_path(self) -> str:
        return str(REPO_FONTS / "gen-ei-mono-go" / self._gen_ei_mono_go)

    def jbm_path(self) -> str:
        return str(REPO_FONTS / "jetbrains-mono" / self._jetbrains_mono)
