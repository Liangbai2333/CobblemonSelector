import json

import requests
from bs4 import BeautifulSoup
from nonebot import require
from nonebot.plugin import PluginMetadata

from plugins.pokemon import pokemon_container, Pokemon

require("pokemon")

__plugin_meta__ = PluginMetadata(
    name="test",
    description="",
    usage="",
)

import requests
import os

# fails = ['Pichu Alola-Bias', 'Cyndaquil Hisui-Bias', 'Quilava Hisui-Bias', 'Unown B', 'Unown C', 'Unown D', 'Unown E',
#          'Unown F', 'Unown G', 'Unown H', 'Unown I', 'Unown J', 'Unown K', 'Unown L', 'Unown M', 'Unown N', 'Unown O',
#          'Unown P', 'Unown Q', 'Unown R', 'Unown S', 'Unown T', 'Unown U', 'Unown V', 'Unown W', 'Unown X', 'Unown Y',
#          'Unown Z', 'Unown !', 'Unown ?', 'Petilil Hisui-Bias', 'Dewott Hisui-Bias', 'Rufflet Hisui-Bias',
#          'Oshawott Hisui-Bias', 'Genesect Water', 'Genesect Electric', 'Genesect Fire', 'Genesect Ice', 'Garbodor Gmax',
#          'Basculin Blue-Striped', 'Basculin White-Striped', 'Mime Jr. Galar-Bias', 'Mime Jr. Galar-Bias',
#          'Arceus Fighting', 'Arceus Flying', 'Arceus Poison', 'Arceus Ground', 'Arceus Rock', 'Arceus Bug',
#          'Arceus Ghost', 'Arceus Steel', 'Arceus Fire', 'Arceus Water', 'Arceus Grass', 'Arceus Electric',
#          'Arceus Psychic', 'Arceus Ice', 'Arceus Dragon', 'Arceus Dark', 'Arceus Fairy', 'Melmetal Gmax',
#          'Ursaluna Bloodmoon', 'Basculegion F', 'Flabebe Yellow', 'Flabebe Orange', 'Flabebe Blue', 'Flabebe White',
#          'Flabebe Flabebe', 'Goomy Hisui-Bias', 'Vivillon Pokeball', 'Meowstic F', 'Furfrou Debutante',
#          'Furfrou Matron', 'Furfrou Dandy', 'Furfrou La-Reine', 'Furfrou Kabuki', 'Furfrou Pharaoh',
#          'Bergmite Hisui-Bias', 'Xerneas Active', 'Pumpkaboo Small', 'Pumpkaboo Large', 'Pumpkaboo Super',
#          'Gourgeist Small', 'Gourgeist Large', 'Gourgeist Super', 'Greninja Bond', 'Zygarde 10%-C', 'Zygarde 50%-C',
#          'Cubone Alola-Bias', 'Eevee Gmax', 'Mr. Mime Galar', 'Mr. Mime Mr. Mime', 'Mr. Mime Galar',
#          'Mr. Mime Mr. Mime', 'Venusaur Gmax', 'Koffing Galar-Bias', 'Snorlax Gmax', 'Exeggcute Alola-Bias',
#          'Kingler Gmax', 'Meowth Gmax', 'Nidoran-M Nidoran-M', 'Nidoran-M Nidoran-M', 'Butterfree Gmax',
#          'Tauros Paldea-Combat', 'Tauros Paldea-Blaze', 'Tauros Paldea-Aqua', 'Lapras Gmax', 'Farfetchâ€™d Galar',
#          'Farfetchâ€™d Galar', 'Pikachu Gmax',
#          'Pikachu Alola-Bias', 'Charizard Mega-X', 'Charizard Mega-Y', 'Charizard Gmax', 'Gengar Gmax',
#          'Blastoise Gmax', 'Mewtwo Mega-X', 'Mewtwo Mega-Y', 'Nidoran-F Nidoran-F', 'Nidoran-F Nidoran-F',
#          'Machamp Gmax', 'Centiskorch Gmax', 'Polteageist Antique', 'Coalossal Gmax', 'Copperajah Gmax',
#          'Cinderace Gmax', 'Toxtricity Low-Key', 'Toxtricity Gmax', 'Toxtricity Low-Key-Gmax', 'Zamazenta Crowned',
#          'Appletun Gmax', 'Rillaboom Gmax', 'Orbeetle Gmax', 'Mr. Rime Mr. Rime', 'Mr. Rime Mr. Rime', 'Inteleon Gmax',
#          'Sirfetchâ€™d Sirfetchâ€™d', 'Sirfetchâ€™d Sirfetchâ€™d', 'Eiscue Noice-Face', 'Hatterene Gmax',
#          'Sinistea Antique', 'Alcremie Ruby-Cream', 'Alcremie Matcha-Cream', 'Alcremie Mint-Cream',
#          'Alcremie Lemon-Cream', 'Alcremie Salted-Cream', 'Alcremie Ruby-Swirl', 'Alcremie Caramel-Swirl',
#          'Alcremie Rainbow-Swirl', 'Alcremie Gmax', 'Grimmsnarl Gmax', 'Indeedee F', 'Corviknight Gmax',
#          'Duraludon Gmax', 'Urshifu Rapid-Strike', 'Urshifu Gmax', 'Urshifu Rapid-Strike-Gmax', 'Zacian Crowned',
#          'Drednaw Gmax', 'Sandaconda Gmax', 'Flapple Gmax', 'Dudunsparce Three-Segment', 'Gouging Fire Gouging Fire',
#          'Gouging Fire Gouging Fire', 'Brute Bonnet Brute Bonnet', 'Brute Bonnet Brute Bonnet',
#          'Iron Thorns Iron Thorns', 'Iron Thorns Iron Thorns', 'Iron Leaves Iron Leaves', 'Iron Leaves Iron Leaves',
#          'Iron Boulder Iron Boulder', 'Iron Boulder Iron Boulder', 'Great Tusk Great Tusk', 'Great Tusk Great Tusk',
#          'Sandy Shocks Sandy Shocks', 'Sandy Shocks Sandy Shocks', 'Walking Wake Walking Wake',
#          'Walking Wake Walking Wake', 'Iron Valiant Iron Valiant', 'Iron Valiant Iron Valiant',
#          'Iron Treads Iron Treads', 'Iron Treads Iron Treads', 'Roaring Moon Roaring Moon', 'Roaring Moon Roaring Moon',
#          'Iron Crown Iron Crown', 'Iron Crown Iron Crown', 'Iron Bundle Iron Bundle', 'Iron Bundle Iron Bundle',
#          'Flutter Mane Flutter Mane', 'Flutter Mane Flutter Mane', 'Poltchageist Artisan', 'Sinistcha Masterpiece',
#          'Scream Tail Scream Tail', 'Scream Tail Scream Tail', 'Raging Bolt Raging Bolt', 'Raging Bolt Raging Bolt',
#          'Ogerpon Wellspring', 'Ogerpon Hearthflame', 'Ogerpon Cornerstone', 'Ogerpon Teal-Tera',
#          'Ogerpon Wellspring-Tera', 'Ogerpon Hearthflame-Tera', 'Ogerpon Cornerstone-Tera', 'Oinkologne F',
#          'Iron Moth Iron Moth', 'Iron Moth Iron Moth', 'Slither Wing Slither Wing', 'Slither Wing Slither Wing',
#          'Iron Hands Iron Hands', 'Iron Hands Iron Hands', 'Iron Jugulis Iron Jugulis', 'Iron Jugulis Iron Jugulis',
#          'Necrozma Dusk-Mane', 'Necrozma Dawn-Wings', 'Oricorio Paâ€™u', 'Rockruff Dusk', 'Type: Null Type: Null',
#          'Type: Null Type: Null', 'Tapu Koko Tapu Koko', 'Tapu Koko Tapu Koko', 'Minior Meteor', 'Tapu Lele Tapu Lele',
#          'Tapu Lele Tapu Lele', 'Tapu Bulu Tapu Bulu', 'Tapu Bulu Tapu Bulu', 'Dartrix Hisui-Bias', 'Silvally Fighting',
#          'Silvally Flying', 'Silvally Poison', 'Silvally Ground', 'Silvally Rock', 'Silvally Bug', 'Silvally Ghost',
#          'Silvally Steel', 'Silvally Fire', 'Silvally Water', 'Silvally Grass', 'Silvally Electric', 'Silvally Psychic',
#          'Silvally Ice', 'Silvally Dragon', 'Silvally Dark', 'Silvally Fairy', 'Tapu Fini Tapu Fini',
#          'Tapu Fini Tapu Fini', 'Rowlet Hisui-Bias'
#          ]


def download_image(url, save_path):
    """
    下载图片并保存到指定路径

    参数:
    url (str): 图片的URL地址
    save_path (str): 保存图片的本地路径
    """
    try:
        # 发送 GET 请求获取图片内容
        response = requests.get(url, stream=True)

        # 检查请求是否成功
        if response.status_code == 200:
            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # 以二进制写入模式打开文件并保存图片内容
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print(f"图片已成功下载并保存到 {save_path}")
        else:
            print(f"下载失败，状态码: {response.status_code}")

    except Exception as e:
        print(f"下载过程中发生错误: {e}")

# save_location = "images/downloaded_image.jpg"  # 保存路径
# container = pokemon_container
# fail_list = []
# for pokemon in container.values():
#     if not isinstance(pokemon, Pokemon):
#         continue
#     all_forms = pokemon.forms + [pokemon]
#     for form in all_forms:
#         save_location = f"images/{pokemon.name}/{form.name}.png"
#         if f"{pokemon.name} {form.name}" in fails or os.path.exists(save_location):
#             continue
#         print(f"开始寻找 {pokemon.name} -> {form.name} 的图片")
#         def select_image_url(poke_url) -> None | str:
#             _response = requests.get(poke_url)
#             _soup = BeautifulSoup(_response.text, "lxml")
#             img_element = _soup.select(".fullImageLink>a:first-child")
#             if img_element:
#                 _image_url = img_element[0].get("href")
#                 if not _image_url.startswith("https:"):
#                     _image_url = f"https:{_image_url}"
#                 return _image_url
#             return None
#         pokedex = form.get_pokedex()
#         if form.name == pokemon.name:
#             name_form = pokemon.name
#         else:
#             name_form = f"{pokemon.name}-{form.name.replace(" ", "_")}"
#         name_form = name_form.replace(" ", "")
#         image_url = select_image_url(f"https://bulbapedia.bulbagarden.net/wiki/File:{pokedex}{name_form}.png")
#         if not image_url:
#             image_url = select_image_url(f"https://wiki.52poke.com/wiki/File:{pokedex}{name_form}.png")
#         if not image_url:
#             name_form = name_form.replace("-", "_")
#             image_url = select_image_url(f"https://bulbapedia.bulbagarden.net/wiki/File:{pokedex}{name_form}.png")
#         if not image_url:
#             image_url = select_image_url(f"https://wiki.52poke.com/wiki/File:{pokedex}{name_form}.png")
#         if not image_url:
#             name_form = name_form.replace("_", "-")
#             image_url = select_image_url(f"https://bulbapedia.bulbagarden.net/wiki/File:{pokedex}{name_form}.png")
#         if not image_url:
#             image_url = select_image_url(f"https://wiki.52poke.com/wiki/File:{pokedex}{name_form}.png")
#         if image_url:
#             download_image(image_url, save_location)
#             print(f"宝可梦 {pokemon.name} -> {form.name} 图片已成功下载并保存到 {save_location}")
#         else:
#             print(f"未找到宝可梦 {pokemon.name} -> {form.name} 图片")
#             fail_list.append(f"{pokemon.name} {form.name}")
# print(fail_list)

#
# impl_aspects = {}
#
# for pokemon in pokemon_container.values():
#     if not isinstance(pokemon, Pokemon):
#         continue
#
#     all_forms = [pokemon] + pokemon.forms
#
#     for form in all_forms:
#         for aspect in form.aspects:
#             if aspect not in impl_aspects:
#                 impl_aspects[f"cobblemon.form.aspect.{aspect}"] = aspect
#
#
# print(json.dumps(impl_aspects, indent=4))




