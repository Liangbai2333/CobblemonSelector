from nonebot import get_plugin_config, require
from nonebot.plugin import PluginMetadata

from .config import Config
from .species.container import pokemon_container
from .species.pokemon import Pokemon

require("nonebot_plugin_htmlrender")

__plugin_meta__ = PluginMetadata(
    name="pokemon",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from plugins.pokemon.loader import loader

container = pokemon_container
#
# print(container["urshifu wushu_style=rapid_strike"].get_full_i18n_name())
# print(container["urshifu wushu_style=single_strike"].get_full_i18n_name())

# print(f"{container['meowth alolan'].get_full_name()} {[biome.get_i18n_name() for biome in container["meowth alolan"].get_spawn_biomes()]}")

# for pokemon in container.values():
#     if (len(pokemon.aspects)) > 1:
#         print(pokemon.name)
#
#     if isinstance(pokemon, Pokemon):
#         for form in pokemon.forms:
#             print(f"{form.get_spawn_biomes()}")

