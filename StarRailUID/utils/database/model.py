from typing import Optional

from fastapi_amis_admin.amis.components import PageSchema
from gsuid_core.utils.database.base_models import Push
from gsuid_core.webconsole import site
from gsuid_core.webconsole.mount_app import GsAdminModel
from sqlmodel import Field


class SrPush(Push, table=True):
    bot_id: str = Field(title="平台")
    sr_uid: str = Field(default=None, title="星铁UID")

    stamina_push: Optional[str] = Field(
        title="体力推送",
        default="off",
        schema_extra={"json_schema_extra": {"hint": "sr开启体力"}},
    )
    stamina_value: Optional[int] = Field(title="体力阈值", default=180)
    stamina_is_push: Optional[str] = Field(title="体力是否已推送", default="off")
    go_push: Optional[str] = Field(
        title="派遣推送",
        default="off",
        schema_extra={"json_schema_extra": {"hint": "sr开启派遣"}},
    )
    go_is_push: Optional[str] = Field(title="派遣是否已推送", default="off")


@site.register_admin
class SrPushAdmin(GsAdminModel):
    pk_name = "id"
    page_schema = PageSchema(label="星铁推送管理", icon="fa fa-bullhorn")  # type: ignore

    # 配置管理模型
    model = SrPush
