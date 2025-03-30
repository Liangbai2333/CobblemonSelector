import time

from nonebot import logger, on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg

from plugins.pokedex.search_biome import search_biome
from plugins.pokedex.util import screenshot

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
    results = search_biome(biome_name)
    logger.info(f"搜索用时: {time.time() - start_time:.2f}秒")
    if not results:
        await matcher.finish("找不到这个群系")

    biome = results[0][0]
    await matcher.finish(
        MessageSegment.image(await screenshot(f"biome/{biome.translation_name}"))
    )