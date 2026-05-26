from collections.abc import Sequence
from typing import Protocol

from PIL import Image, ImageDraw


class MonthlyGroup(Protocol):
    action_name: str
    percent: int


COLOR_MAP = {
    "每日活跃": (248, 227, 157),
    "活动奖励": (99, 231, 176),
    "冒险奖励": (114, 205, 251),
    "模拟宇宙奖励": (160, 149, 248),
    "忘却之庭奖励": (221, 119, 250),
    "邮件奖励": (244, 110, 104),
    "周期积分奖励": (247, 178, 97),
    "其他": (255, 242, 200),
    "Daily Activity": (248, 227, 157),
    "Events": (99, 231, 176),
    "Adventure": (114, 205, 251),
    "moni": (160, 149, 248),
    "Spiral Abyss": (221, 119, 250),
    "Quests": (244, 110, 104),
    "Other": (255, 242, 200),
}
UNKNOWN_GROUP_COLOR = COLOR_MAP["其他"]


def draw_monthly_pie(group_by: Sequence[MonthlyGroup]) -> Image.Image:
    """Draw a monthly award chart while accepting new server-side categories."""
    xy = ((0, 0), (2100, 2100))
    pie_image = Image.new("RGBA", (2100, 2100), color=(255, 255, 255, 0))
    pie_image_draw = ImageDraw.Draw(pie_image)
    if not group_by:
        pie_image_draw.ellipse(xy, fill=(128, 128, 128))
    else:
        angle = -90
        for item in group_by:
            end_angle = angle + (item.percent / 100) * 360
            pie_image_draw.pieslice(
                xy,
                angle,
                end_angle,
                COLOR_MAP.get(item.action_name, UNKNOWN_GROUP_COLOR),
            )
            angle = end_angle

    pie_image_draw.ellipse((150, 150, 1950, 1950), fill=(255, 255, 255, 0))
    return pie_image.resize((210, 210))
