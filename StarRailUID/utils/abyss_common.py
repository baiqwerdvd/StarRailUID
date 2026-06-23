from typing import List, Optional, Tuple

from PIL import Image

from ..sruid_utils.api.mys.models import AbyssFloorDetail, AbyssNodeDetail

NODE_PART_HEIGHT = 219
FLOOR_BASE_HEIGHT = 570


def has_node_3(level: AbyssFloorDetail) -> bool:
    return level.node_3 is not None and bool(level.node_3.avatars)


def get_floor_nodes(level: AbyssFloorDetail) -> List[Tuple[int, AbyssNodeDetail]]:
    nodes = [(1, level.node_1), (2, level.node_2)]
    if has_node_3(level):
        assert level.node_3 is not None
        nodes.append((3, level.node_3))
    return nodes


def is_fast_floor(level: AbyssFloorDetail) -> bool:
    if level.is_fast:
        return True
    nodes = [level.node_1, level.node_2]
    if level.node_3 is not None:
        nodes.append(level.node_3)
    return all(not node.avatars for node in nodes)


def floor_height(level: AbyssFloorDetail) -> int:
    if has_node_3(level):
        return FLOOR_BASE_HEIGHT + NODE_PART_HEIGHT
    return FLOOR_BASE_HEIGHT


def extend_floor_pic(floor_pic: Image.Image, level: AbyssFloorDetail) -> Image.Image:
    target_h = floor_height(level)
    if floor_pic.height >= target_h:
        return floor_pic
    extended = Image.new("RGBA", (floor_pic.width, target_h), (0, 0, 0, 0))
    extended.paste(floor_pic, (0, 0))
    return extended


def calc_sum_score(level: AbyssFloorDetail) -> Optional[int]:
    scores: List[int] = []
    for _, node in get_floor_nodes(level):
        if node.score:
            scores.append(int(node.score))
    if len(scores) == len(get_floor_nodes(level)):
        return sum(scores)
    return None


def format_star_text(star_num: int, max_star: int, extra_star_num: int = 0) -> str:
    text = f"{star_num}/{max_star}"
    if extra_star_num > 0:
        text += f" 星启{extra_star_num}"
    return text
