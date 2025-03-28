from nonebot import require, logger
from nonebot.plugin import PluginMetadata

require("pokemon")

__plugin_meta__ = PluginMetadata(
    name="pokedex",
    description="",
    usage="",
)

from plugins.pokedex.search_pokemon import build_pokemon_index
from plugins.pokedex.search_biome import build_biome_index

logger.info("开始建立索引...")
import time
start = time.time()
build_pokemon_index()
build_biome_index()
logger.info(f"索引建立完成，用时: {time.time() - start:.2f}秒")

from plugins.pokedex import dex, spawn, biome, biome_list