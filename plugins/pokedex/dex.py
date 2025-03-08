import time

from nonebot import logger, on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg
from nonebot_plugin_htmlrender import template_to_pic

from plugins.pokedex.search import search_pokemon
from plugins.pokemon.path import resolve

c = on_command("图鉴", aliases={"pokedex", "dex"}, block=True)

@c.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    """
    测试
    """
    if arg.extract_plain_text():
        matcher.set_arg("pokemon_name", arg)



@c.got("pokemon_name", prompt="请输入要查询的 Pokémon")
async def _(matcher: Matcher, pokemon_name: str = ArgPlainText()):
    start_time = time.time()
    results = search_pokemon(pokemon_name)
    logger.info(f"搜索用时: {time.time() - start_time:.2f}秒")
    if not results:
        await matcher.finish("找不到这个 Pokémon")

    poke = results[0][0]
    pic = await template_to_pic(resolve(
        "templates/pokedex"
    ), "pokemon_detail.html", {
        "pokemon": poke
    })
    await matcher.finish(MessageSegment.image(pic))