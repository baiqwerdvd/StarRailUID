from pathlib import Path

from PIL import Image
from gsuid_core.models import Event
from gsuid_core.utils.image.image_tools import CustomizeImage, get_event_avatar

from ..resource.RESOURCE_PATH import CHAR_ICON_PATH, CU_BG_PATH

BG_PATH = Path(__file__).parent / "bg"
NM_BG_PATH = BG_PATH / "nm_bg"
TEXT_PATH = Path(__file__).parent / "texture2d"
NATURE_ICON_PATH = Path(__file__).parent / "icon_nature"

elements = {
    "ice": Image.open(NATURE_ICON_PATH / "IconNatureColorIce.png").convert("RGBA"),
    "fire": Image.open(NATURE_ICON_PATH / "IconNatureColorFire.png").convert("RGBA"),
    "imaginary": Image.open(NATURE_ICON_PATH / "IconNatureColorImaginary.png").convert("RGBA"),
    "quantum": Image.open(NATURE_ICON_PATH / "IconNatureColorQuantum.png").convert("RGBA"),
    "lightning": Image.open(NATURE_ICON_PATH / "IconNatureColorThunder.png").convert("RGBA"),
    "wind": Image.open(NATURE_ICON_PATH / "IconNatureColorWind.png").convert("RGBA"),
    "physical": Image.open(NATURE_ICON_PATH / "IconNaturePhysical.png").convert("RGBA"),
}


def _get_bg_path() -> Path:
    if CU_BG_PATH.exists() and any(CU_BG_PATH.iterdir()):
        return CU_BG_PATH
    return NM_BG_PATH


async def get_simple_bg(based_w: int, based_h: int, image: str | None | Image.Image = None) -> Image.Image:
    CIL = CustomizeImage(_get_bg_path())
    return CIL.get_image(image, based_w, based_h)


def get_footer():
    return Image.open(TEXT_PATH / "footer.png")


async def _get_event_avatar(event: Event) -> Image.Image:
    return await get_event_avatar(event, CHAR_ICON_PATH)
