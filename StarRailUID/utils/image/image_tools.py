from pathlib import Path
from typing import Union

from gsuid_core.models import Event
from gsuid_core.utils.image.image_tools import CustomizeImage, get_event_avatar
from PIL import Image

from ..resource.RESOURCE_PATH import CHAR_ICON_PATH, CU_BG_PATH

BG_PATH = Path(__file__).parent / "bg"
NM_BG_PATH = BG_PATH / "nm_bg"
TEXT_PATH = Path(__file__).parent / "texture2d"
NATURE_ICON_PATH = Path(__file__).parent / "icon_nature"

elements = {
    "ice": Image.open(NATURE_ICON_PATH / "IconNatureColorIce.png").convert("RGBA"),
    "fire": Image.open(NATURE_ICON_PATH / "IconNatureColorFire.png").convert("RGBA"),
    "imaginary": Image.open(NATURE_ICON_PATH / "IconNatureColorImaginary.png").convert(
        "RGBA"
    ),
    "quantum": Image.open(NATURE_ICON_PATH / "IconNatureColorQuantum.png").convert(
        "RGBA"
    ),
    "lightning": Image.open(NATURE_ICON_PATH / "IconNatureColorThunder.png").convert(
        "RGBA"
    ),
    "wind": Image.open(NATURE_ICON_PATH / "IconNatureColorWind.png").convert("RGBA"),
    "physical": Image.open(NATURE_ICON_PATH / "IconNaturePhysical.png").convert("RGBA"),
}

if list(CU_BG_PATH.iterdir()) != []:
    bg_path = CU_BG_PATH
else:
    bg_path = NM_BG_PATH

if list(CU_BG_PATH.iterdir()) != []:
    bg_path = CU_BG_PATH
else:
    bg_path = NM_BG_PATH


async def get_simple_bg(
    based_w: int, based_h: int, image: Union[str, None, Image.Image] = None
) -> Image.Image:
    CIL = CustomizeImage(NM_BG_PATH)
    return CIL.get_image(image, based_w, based_h)


def get_footer():
    return Image.open(TEXT_PATH / "footer.png")


async def _get_event_avatar(event: Event) -> Image.Image:
    return await get_event_avatar(event, CHAR_ICON_PATH)
