from gsuid_core.utils.plugins_config.gs_config import StringConfig

from .config_default import CONFIG_DEFAULT
from ..utils.resource.RESOURCE_PATH import CONFIG_PATH

srconfig = StringConfig(
    "StarRailUID",
    CONFIG_PATH,
    CONFIG_DEFAULT,
)
