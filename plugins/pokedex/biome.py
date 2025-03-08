import time

from nonebot import logger, on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg
from nonebot_plugin_htmlrender import template_to_pic

from plugins.pokedex.search_pokemon import search_pokemon
from plugins.pokemon.loader.data import biome_map
from plugins.pokemon.path import resolve


c = on_command("群系", aliases={"biome"}, block=True)

@c.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    """
    测试
    """
    if arg.extract_plain_text():
        matcher.set_arg("biome_name", arg)



@c.got("biome_name", prompt="请输入要查询的群系")
async def _(matcher: Matcher, biome_name: str = ArgPlainText()):
    start_time = time.time()
    biome = biome_map.get(biome_name, None)
    logger.info(f"搜索用时: {time.time() - start_time:.2f}秒")
    if not biome:
        await matcher.finish("找不到这个群系")

    pic = await template_to_pic(resolve(
        "templates/biome"
    ), "biome_detail.html", {
        "biome": biome
    })
    await matcher.finish(MessageSegment.image(pic))