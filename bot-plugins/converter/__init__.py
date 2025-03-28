import json
import os.path
import re
from typing import Any, Optional

import yaml
from nonebot import require
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.internal.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.plugin.on import on_command
from pydantic import BaseModel, Field

__plugin_meta__ = PluginMetadata(
    name="converter",
    description="",
    usage="",
)

from plugins.pokemon.spawn_pool.pool import SpawnPool

moon_phase_converter = {
    "满月": "0",
    "亏凸月": "1",
    "下弦月": "2",
    "残月": "3",
    "新月": "4",
    "蛾眉月": "5",
    "上弦月": "6",
    "盈凸月": "7"
}

range_name = {
    "白天": "day",
    "夜晚": "night",
    "中午": "noon",
    "午夜": "midnight",
    "黎明": "dawn",
    "黄昏": "dusk",
    "上午": "morning",
    "下午": "afternoon"
}

def convert_weather(weathers: list[str], condition):
    for weather in weathers:
        if weather == "晴天":
            condition.isRaining = False
            condition.isThundering = False
        elif weather == "雨天":
            condition.isRaining = True
            condition.isThundering = False
        elif weather == "雷雨天":
            condition.isRaining = True
            condition.isThundering = True
        else:
            raise ValueError(f"未知天气类型: {weather}")


  # id: 雷公
  # specie: Raikou
  # localizedName: '&6雷公'
  # limitGroup: 默认组
  # extra: lvl:70
  # times:
  # - 黎明
  # - 上午
  # biomes:
  # - 破碎的热带高原
  # - 热带草原
  # - 热带高原
  # - 破碎的热带草原
  # weathers: []
  # moonPhases: []
  # locations:
  # - 陆地
  # rarity: 3.0
  # fakeRarity: 3.55
class SpawnInfo(BaseModel):
    specie: str
    extra: str
    times: list[str] = []
    biomes: list[str] = []
    weathers: list[str] = []
    moonPhases: list[str] = []
    locations: list[str] = []
    rarity: float

    level: Optional[str] = Field(default=None, exclude=True)

c = on_command("转换", block=True)

@c.handle()
async def _(matcher: Matcher, event: MessageEvent):
    require("pokemon")
    require("pokedex")

    from plugins.pokedex.search_pokemon import search_pokemon
    from plugins.pokedex.search_biome import search_biome

    from plugins.pokemon.spawn_pool.bucket import get_bucket
    from plugins.pokemon.spawn_pool.condition import SpawnCondition
    from plugins.pokemon.spawn_pool.detail import SpawnDetail
    from plugins.pokemon.species.pokemon import PokemonForm
    if not event.sender.user_id == 1739566851:
        matcher.finish("你没有权限使用这个命令")
    path = os.path.join(os.path.dirname(__file__), "spawn.yml")
    spawn: dict[str, Any] = yaml.load(open(path, "r", encoding="utf-8"), Loader=yaml.FullLoader)
    spawn_infos = []
    for spawn_info in spawn.values():
        info = SpawnInfo(**spawn_info)
        info.specie = info.specie.lower()
        info.level = re.search(r"lvl:\s?(\d+)", info.extra).group(1)
        spawn_infos.append(info)

    for spawn_info in spawn_infos:
        pokemon_matched = search_pokemon(spawn_info.specie)
        if not pokemon_matched:
            await matcher.send(f"[严重] 无法匹配的品种: {spawn_info.specie}")

        matched = pokemon_matched[0]
        pokemon: PokemonForm = matched[0]

        name = f"{pokemon.original_name} {' '.join(pokemon.aspects)}".strip()

        biomes = []
        for biome in spawn_info.biomes:
            biome_matched = search_biome(biome)
            if not biome_matched:
                await matcher.send(f"[严重] [{pokemon.get_full_i18n_name()}] 无法匹配的生物群系: {biome}")
                continue
            matched = biome_matched[0]
            biome_obj = matched[0]
            if matched[1] < 0.58:
                await matcher.send(f"[警告] [{pokemon.get_full_i18n_name()}] 匹配的生物群系与原版有较大差异: 匹配结果： {biome_obj.get_i18n_name()} 源: {biome}")
            if biome_obj not in biomes:
                biomes.append(biome_obj)

        times = []
        for time in spawn_info.times:
            if time not in range_name:
                await matcher.send(f"[严重] [{pokemon.get_full_i18n_name()}] 无法匹配的时间: {time}")
                continue
            times.append(range_name[time])

        moon_phases = []
        for moonPhase in spawn_info.moonPhases:
            if moonPhase not in moon_phase_converter:
                await matcher.send(f"[严重] [{pokemon.get_full_i18n_name()}] 无法匹配的月相: {moonPhase}")
                continue
            moon_phases.append(moon_phase_converter[moonPhase])

        details = []

        if not times:
            condition = SpawnCondition(
                biomes=biomes,
                moonPhase=",".join(moon_phases) if moon_phases else None
            )
            convert_weather(spawn_info.weathers, condition)
            detail = SpawnDetail(
                enabled=True,
                pokemon=name,
                context="grounded",
                bucket=get_bucket("ultra-rare"),
                level=spawn_info.level,
                weight=spawn_info.rarity,
                condition=condition
            )
            details.append(detail)

        for time in times:
            condition = SpawnCondition(
                timeRange=time,
                biomes=biomes,
                moonPhase=",".join(moon_phases) if moon_phases else None
            )
            convert_weather(spawn_info.weathers, condition)
            detail = SpawnDetail(
                enabled=True,
                pokemon=name,
                context="grounded",
                bucket=get_bucket("ultra-rare"),
                level=spawn_info.level,
                weight=spawn_info.rarity,
                condition=condition
            )
            details.append(detail)

        dex = f"0{pokemon.get_pokedex()}" if len(pokemon.get_pokedex()) <= 3 else pokemon.get_pokedex()
        save_file_path = os.path.join(os.path.dirname(__file__),
                                      f"saves/{dex}_{pokemon.original_name}.json")
        spawn_pool = SpawnPool(
            enabled=True,
            spawns=details
        )

        def deep_remove_none(obj: Any) -> Any:
            """递归移除字典、列表和其他容器中的None值"""
            if isinstance(obj, dict):
                # 处理字典：过滤None值并递归处理剩余值
                return {k: deep_remove_none(v) for k, v in obj.items() if v is not None}
            elif isinstance(obj, list):
                # 处理列表：递归处理每个元素
                return [deep_remove_none(item) for item in obj if item is not None]
            elif isinstance(obj, tuple):
                # 处理元组：递归处理每个元素并重新创建元组
                return tuple(deep_remove_none(item) for item in obj if item is not None)
            elif isinstance(obj, set):
                # 处理集合：递归处理每个元素并重新创建集合
                return {deep_remove_none(item) for item in obj if item is not None}
            else:
                # 基本类型直接返回
                return obj
        # json_data = spawn_pool.model_dump_json(indent=4, exclude_none=True, exclude_defaults=True, exclude_unset=True)
        spawn_dict = spawn_pool.model_dump(exclude_defaults=True, exclude_unset=True)
        with open(save_file_path, "w", encoding="utf-8") as f:
            json.dump(deep_remove_none(spawn_dict), f, ensure_ascii=False, indent=4)






