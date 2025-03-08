from nonebot import require, on_command, logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot_plugin_htmlrender import template_to_pic

from plugins.pokemon.path import resolve

require("pokemon")

__plugin_meta__ = PluginMetadata(
    name="pokedex",
    description="",
    usage="",
)

from plugins.pokedex.search_pokemon import build_pokemon_index

logger.info("开始建立索引...")
import time
start = time.time()
pokemon_index = build_pokemon_index()
logger.info(f"索引建立完成，用时: {time.time() - start:.2f}秒")

from plugins.pokedex import dex, spawn, biome