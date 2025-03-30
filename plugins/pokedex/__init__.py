from nonebot import require, logger, get_plugin_config
from nonebot.plugin import PluginMetadata

from plugins.pokedex.config import Config

require("pokemon")

__plugin_meta__ = PluginMetadata(
    name="pokedex",
    description="",
    usage="",
)

config = get_plugin_config(Config)

from plugins.pokedex.search_pokemon import build_pokemon_index
from plugins.pokedex.search_biome import build_biome_index

logger.info("开始建立索引...")
import time
start = time.time()
build_pokemon_index()
build_biome_index()
logger.info(f"索引建立完成，用时: {time.time() - start:.2f}秒")

from plugins.pokedex import dex, spawn, biome, biome_list