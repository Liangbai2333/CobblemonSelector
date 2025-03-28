from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.plugin.on import on_command
from nonebot_plugin_htmlrender import template_to_pic

from plugins.pokemon.biome.biome import Biome
from plugins.pokemon.loader.data import biome_map
from plugins.pokemon.path import resolve


def sort_biomes(biome_list: list[Biome]):
    """
    对包含中文和英文的字符串列表进行排序
    中文在前（按拼音字母顺序），英文在后（按英文字母顺序）

    参数:
        string_list: 包含中文和英文的字符串列表
    返回:
        排序后的列表
    """
    import re

    # 判断字符串是否只包含英文字符
    def is_english(text):
        return bool(re.match(r'^[a-zA-Z0-9\s.,!?#;_:\'\"()\[\]{}]+$', text))

    # 使用拼音排序中文
    try:
        from pypinyin import pinyin, Style

        # 获取字符串的拼音用于排序
        def get_pinyin(text):
            if is_english(text):
                return text.lower()
            else:
                # 将中文转换为拼音，用于排序
                result = pinyin(text, style=Style.NORMAL)
                return ''.join([''.join(p) for p in result])

        # 分别获取中文和英文对象
        chinese_objects = [biome for biome in biome_list if not is_english(biome.get_i18n_name())]
        english_objects = [biome for biome in biome_list if is_english(biome.get_i18n_name())]
        # 对中文对象按拼音排序
        sorted_chinese = sorted(chinese_objects, key=lambda obj: get_pinyin(obj.get_i18n_name()))
        # 对英文对象按字母排序
        sorted_english = sorted(english_objects, key=lambda obj: obj.get_i18n_name().lower())

        # 合并结果：中文在前，英文在后
        return sorted_chinese + sorted_english

    except ImportError:
        print("请安装pypinyin库: pip install pypinyin")
        return biome_list

biomes = sort_biomes(list(filter(lambda biome: len(biome.details) > 0, set(biome_map.values()))))


c = on_command("所有群系", aliases={"全部群系", "群系列表", "全群系", "群系全"}, block=True)


@c.handle()
async def _(matcher: Matcher):
    pic = await template_to_pic(resolve(
        "templates/biome"
    ), "biome_list.html", {
        "biomes": biomes
    })
    await matcher.finish(MessageSegment.image(pic))