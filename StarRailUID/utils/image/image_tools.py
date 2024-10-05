from pathlib import Path
from typing import Union

from PIL import Image
from gsuid_core.utils.image.image_tools import CustomizeImage

from ..resource.RESOURCE_PATH import CU_BG_PATH

BG_PATH = Path(__file__).parent / "bg"
NM_BG_PATH = BG_PATH / "nm_bg"
TEXT_PATH = Path(__file__).parent / "texture2d"

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
    return Image.open(TEXT_PATH / 'footer.png')
