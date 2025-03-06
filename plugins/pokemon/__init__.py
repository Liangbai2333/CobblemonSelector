from nonebot import get_plugin_config, require, logger
from nonebot.plugin import PluginMetadata

from .config import Config
from .species.container import pokemon_container

require("nonebot_plugin_htmlrender")

__plugin_meta__ = PluginMetadata(
    name="species",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from plugins.pokemon.loader import loader

t = pokemon_container["meowth alolan"]
print(pokemon_container["meowth gmax"].model_dump_json())
print(pokemon_container["meowth gmax"].evolutions[0].requirements[0].model_dump_json())