from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
REPO_FONTS = REPO_ROOT / "fonts"


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
