from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg
from nonebot_plugin_htmlrender import template_to_pic

from plugins.pokemon import load_pokemons, resolve, load_details

pokemons = load_pokemons()
for pokemon in list(pokemons.values()):
     pokemons[pokemon.get_i18n_name()] = pokemon
     pokemons[pokemon.get_pokedex()] = pokemon
     pokemons[str(pokemon.nationalPokedexNumber)] = pokemon
#
#
# details = load_details()
# for detail in list(details.values()):
#     species = detail.get_pokemon()
#     if not detail.is_regional():
#         details[species.get_i18n_name()] = detail
#         details[species.get_pokedex()] = detail
#         details[str(species.nationalPokedexNumber)] = detail
#
#
# detail = on_command("生成", block=True)
# @detail.handle()
# async def _(matcher: Matcher, arg: Message = CommandArg()):
#     if arg.extract_plain_text():
#         matcher.set_arg("pokemon_name", arg)
#
#
# @detail.got("pokemon_name", prompt="请输入要查询的 Pokémon")
# async def _(matcher: Matcher, pokemon_name: str = ArgPlainText()):
#     if pokemon_name not in details:
#         await matcher.finish("找不到这个 Pokémon")
#
#     detail = details[pokemon_name]
#     pic = await template_to_pic(resolve(
#         "templates/spawn"
#     ), "spawn_detail.html", {
#         "spawn_detail": detail
#     })
#     await matcher.finish(MessageSegment.image(pic))


c = on_command("图鉴", aliases={"pokedex"}, block=True)

@c.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    """
    测试
    """
    if arg.extract_plain_text():
        matcher.set_arg("pokemon_name", arg)



@c.got("pokemon_name", prompt="请输入要查询的 Pokémon")
async def _(matcher: Matcher, pokemon_name: str = ArgPlainText()):
    if pokemon_name not in pokemons:
        await matcher.finish("找不到这个 Pokémon")

    poke = pokemons[pokemon_name]
    pic = await template_to_pic(resolve(
        "templates/pokedex"
    ), "pokemon_detail.html", {
        "pokemon": poke
    })
    await matcher.finish(MessageSegment.image(pic))