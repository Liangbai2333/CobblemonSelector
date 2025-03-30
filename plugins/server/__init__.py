from nonebot import require
from nonebot.plugin import PluginMetadata, get_plugin_config

from plugins.server.config import Config

require("pokemon")

__plugin_meta__ = PluginMetadata(
    name="server",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from .server import bootstrap

bootstrap(config.cs_server_port)