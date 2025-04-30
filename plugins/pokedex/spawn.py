import time

from nonebot import logger, on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg

from plugins.pokedex.search_pokemon import search_pokemon
from plugins.pokedex.util import screenshot

c = on_command("生成", aliases={"spawn", "detail"}, block=True)

@c.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    """
    测试
    """
    if text := arg.extract_plain_text():
        args = text.split(" ")
        matcher.set_arg("pokemon_name", Message(args[0]))
        if len(args) == 2:
            if not args[1].isdigit():
                await matcher.finish("请输入正确的索引")
            matcher.set_arg("index", Message(args[1]))
        else:
            matcher.set_arg("index", Message("0"))

@c.got("pokemon_name", prompt="请输入要查询的 Pokémon")
@c.got('index')
async def _(matcher: Matcher, pokemon_name: str = ArgPlainText(), index: str = ArgPlainText()):
    start_time = time.time()
    results = search_pokemon(pokemon_name)
    logger.info(f"搜索用时: {time.time() - start_time:.2f}秒")
    if not results:
        await matcher.finish("找不到这个 Pokémon")

    poke = results[0][0]
    index_num = int(index) - 1

    if not poke.spawn_details:
        await matcher.finish("这个 Pokémon 没有生成数据")

    if index_num >= len(poke.spawn_details):
        await matcher.finish("索引超出最大数量")

    if index_num < -1:
        index_num = poke.spawn_details.index(max(poke.spawn_details, key=lambda x: x.weight))

    await matcher.finish(
        MessageSegment.image(await screenshot(f"spawn/{poke.get_search_name()}/{index_num}", device_scale_factor=3))
    )