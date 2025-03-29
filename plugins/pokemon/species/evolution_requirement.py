from enum import Enum
from typing import Literal, Optional

from pydantic import Field, field_validator, BaseModel, model_serializer
from pydantic_core.core_schema import SerializerFunctionWrapHandler

from plugins.pokemon.extension.type import TypedModel
from plugins.pokemon.lang import get_lang
from plugins.pokemon.loader.data import biome_map
from plugins.pokemon.species.feature import Feature
from plugins.pokemon.species.move import Move


class EvolutionRequirement(TypedModel, type="variant"):
    variant: str = Field(description="进化需求选择器")

    @model_serializer(mode="wrap")
    def serialize(self, nxt: SerializerFunctionWrapHandler):
        serialized = nxt(self)
        serialized["i18n_name"] = self.get_evo_i18n()
        return serialized

    def get_evo_i18n(self) -> str:
        pass


class AnyRequirement(EvolutionRequirement):
    variant: Literal["any"]

    possibilities: list[EvolutionRequirement] = Field(default=[], description="条件，满足其一即可")


class Area(EvolutionRequirement):
    class AABB(BaseModel):
        minX: float = Field(default=0.0, description="最小X坐标")
        minY: float = Field(default=0.0, description="最小Y坐标")
        minZ: float = Field(default=0.0, description="最小Z坐标")
        maxX: float = Field(default=0.0, description="最大X坐标")
        maxY: float = Field(default=0.0, description="最大Y坐标")
        maxZ: float = Field(default=0.0, description="最大Z坐标")

    variant: Literal["area"]

    box: AABB = Field(description="区域")

    def get_evo_i18n(self) -> str:
        return f"在区域[{self.box.minX},{self.box.minY},{self.box.minZ} {self.box.maxX},{self.box.maxY},{self.box.maxZ}]内"


class AttackDefenceRatio(EvolutionRequirement):
    class AttackDefenceRatioEnum(Enum):
        ATTACK_HIGHER = "attack_higher"
        DEFENCE_HIGHER = "defence_higher"
        EQUAL = "equal"

    variant: Literal["attack_defence_ratio"]

    ratio: AttackDefenceRatioEnum = Field(description="比较")

    def get_evo_i18n(self) -> str:
        if self.ratio == self.AttackDefenceRatioEnum.ATTACK_HIGHER:
            return "攻击高于防御"
        elif self.ratio == self.AttackDefenceRatioEnum.DEFENCE_HIGHER:
            return "防御高于攻击"
        else:
            return "攻击等于防御"


class Biome(EvolutionRequirement):
    variant: Literal["biome"]

    biomeCondition: Optional[str] = Field(default=None, description="生物群系条件")
    biomeAnticondition: Optional[str] = Field(default=None, description="不匹配的生物群系条件")

    def get_evo_i18n(self) -> str:
        if self.biomeAnticondition:
            return f"不在{biome_map[self.biomeAnticondition].get_i18n_name()}群系"
        elif self.biomeCondition:
            return f"在{biome_map[self.biomeCondition].get_i18n_name()}群系"
        else:
            return "在任意群系"


class BlocksTraveledRequirement(EvolutionRequirement):
    variant: Literal["blocks_traveled"]

    amount: int = Field(default=0, description="移动距离")

    def get_evo_i18n(self) -> str:
        return f"移动{self.amount}格距离"


class DamageTaken(EvolutionRequirement):
    variant: Literal["damage_taken"]

    amount: int = Field(default=0, description="伤害")

    def get_evo_i18n(self) -> str:
        return f"受到{self.amount}点伤害"


class Defeat(EvolutionRequirement):
    variant: Literal["defeat"]

    target: str = Field(description="目标")
    amount: int = Field(default=0, description="数量")

    def get_evo_i18n(self) -> str:
        from plugins.pokemon import pokemon_container
        pokemon = pokemon_container.get(self.target, None)
        target_name = pokemon.get_i18n_name() if pokemon else self.target
        return f"击败{self.amount}个{target_name}"


class Friendship(EvolutionRequirement):
    variant: Literal["friendship"]

    amount: int = Field(default=0, description="友好度")

    def get_evo_i18n(self) -> str:
        return f"友好度达到{self.amount}"


class HeldItem(EvolutionRequirement):
    variant: Literal["held_item"]

    itemCondition: str = Field(description="道具")

    def get_evo_i18n(self) -> str:
        item_name = self.itemCondition[1:] if self.itemCondition.startswith("#") else self.itemCondition
        (namespace, key) = item_name.split(":")
        return f"持有{get_lang().get(f"item.{namespace}.{key}")}"


class Level(EvolutionRequirement):
    variant: Literal["level"]

    minLevel: int = Field(default=1, description="最小等级")
    maxLevel: int = Field(default=100, description="最大等级")

    def get_evo_i18n(self) -> str:
        return f"达到{self.minLevel}级"


class MoonPhase(EvolutionRequirement):
    variant: Literal["moon_phase"]

    moonPhase: str = Field(description="月相")

    def get_evo_i18n(self) -> str:
        # FULL_MOON,
        # WANING_GIBBOUS,
        # THIRD_QUARTER,
        # WANING_CRESCENT,
        # NEW_MOON,
        # WAXING_CRESCENT,
        # FIRST_QUARTER,
        # WAXING_GIBBOUS;
        if self.moonPhase == "FULL_MOON":
            phase_name = "满月"
        elif self.moonPhase == "WANING_GIBBOUS":
            phase_name = "亏凸月"
        elif self.moonPhase == "THIRD_QUARTER":
            phase_name = "下弦月"
        elif self.moonPhase == "WANING_CRESCENT":
            phase_name = " 残月"
        elif self.moonPhase == "NEW_MOON":
            phase_name = "新月"
        elif self.moonPhase == "WAXING_CRESCENT":
            phase_name = "蛾眉月"
        elif self.moonPhase == "FIRST_QUARTER":
            phase_name = "上弦月"
        elif self.moonPhase == "WAXING_GIBBOUS":
            phase_name = "盈凸月"
        else:
            phase_name = "未知"
        return f"月相为{phase_name}"


class MoveSet(EvolutionRequirement):
    variant: Literal["has_move"]

    move: str = Field(description="招式")

    def get_evo_i18n(self) -> str:
        move_obj = Move(condition="", name=self.move)
        return f"拥有招式{move_obj.get_i18n_name()}"


class MoveType(EvolutionRequirement):
    variant: Literal["has_move_type"]

    type: str = Field(description="招式类型")

    def get_evo_i18n(self) -> str:
        return f"拥有{get_lang().get(f"cobblemon.type.{self.type}")}招式类型"



class PartyMember(EvolutionRequirement):
    variant: Literal["party_member"]

    target: str = Field(description="目标")
    contains: bool = Field(default=True, description="是否包含")

    def get_evo_i18n(self) -> str:
        from plugins.pokemon import pokemon_container
        pokemon = pokemon_container.get(self.target, None)
        target_name = pokemon.get_i18n_name() if pokemon else self.target
        return f"身上{'携带' if self.contains else '不携带'}{target_name}"


class PlayerHasAdvancement(EvolutionRequirement):
    variant: Literal["advancement"]

    requiredAdvancement: str = Field(description="需求成就")

    def get_evo_i18n(self) -> str:
        (namespace, key) = self.requiredAdvancement.split(":")
        return f"拥有成就{get_lang().get(f"advancements.{namespace}.{key}")}"


class PokemonProperties(EvolutionRequirement):
    variant: Literal["properties"]

    target: str = Field(description="目标")

    def get_evo_i18n(self) -> str:
        if self.target.startswith("gender"):
            (_, sex) = self.target.split("=")
            return f"{"雄性" if sex == "male" else "雌性"}"
        if self.target.startswith("nickname"):
            (_, nickname) = self.target.split("=")
            return f"昵称为{nickname}"
        return f"属性具有{self.target}"


class PropertyRange(EvolutionRequirement):
    variant: Literal["property_range"]

    range: tuple[int, int] = Field(description="范围")
    feature: Feature = Field(description="特性")

    def get_evo_i18n(self) -> str:
        return f"{self.feature.get_i18n_name()}在{self.range[0]}到{self.range[1]}之间"


    @field_validator("range", mode="before")
    @classmethod
    def validate_range(cls, value: str) -> tuple[int, int]:
        splits = value.split("-")
        return int(splits[0]), int(splits[1])


class Recoil(EvolutionRequirement):
    variant: Literal["recoil"]

    amount: int = Field(default=0, description="反作用伤害")

    def get_evo_i18n(self) -> str:
        return f"受到{self.amount}点反伤"


class StatCompare(EvolutionRequirement):
    variant: Literal["stat_compare"]

    highStat: str = Field(description="高值")
    lowStat: str = Field(description="低值")

    def get_evo_i18n(self) -> str:
        high_stat_name = get_lang().get(f"cobblemon.stat.{self.highStat}.name")
        low_stat_name = get_lang().get(f"cobblemon.stat.{self.lowStat}.name")
        return f"{high_stat_name}大于{low_stat_name}"


class StatEqual(EvolutionRequirement):
    variant: Literal["stat_equal"]

    statOne: str = Field(description="值1")
    statTwo: str = Field(description="值2")

    def get_evo_i18n(self) -> str:
        stat_one_name = get_lang().get(f"cobblemon.stat.{self.statOne}.name")
        stat_two_name = get_lang().get(f"cobblemon.stat.{self.statTwo}.name")
        return f"{stat_one_name}等于{stat_two_name}"


class Structure(EvolutionRequirement):
    variant: Literal["structure"]

    structureCondition: Optional[str] = Field(default=None, description="结构条件")
    structureAnticondition: Optional[str] = Field(default=None, description="不匹配的结构条件")

    def get_evo_i18n(self) -> str:
        if self.structureCondition:
            return f"满足结构条件{self.structureCondition}"
        elif self.structureAnticondition:
            return f"不满足结构条件{self.structureAnticondition}"
        else:
            return "未知"


class TimeRange(EvolutionRequirement):
    variant: Literal["time_range"]

    range: Literal[
        "any",
        "day",
        "night",
        "noon",
        "midnight",
        "dawn",
        "dusk",
        "twilight",
        "morning",
        "afternoon",
        "predawn",
        "evening"
    ] = Field(description="时间范围")

    def get_evo_i18n(self) -> str:
        range_name = {
            "any": "任意",
            "day": "白天",
            "night": "黑夜",
            "noon": "中午",
            "midnight": "午夜",
            "dawn": "黎明",
            "dusk": "黄昏",
            "twilight": "黄昏",
            "morning": "早上",
            "afternoon": "下午",
            "predawn": "凌晨",
            "evening": "晚上"
        }.get(self.range, "未知")
        return f"时间为{range_name}"


class UseMove(EvolutionRequirement):
    variant: Literal["use_move"]

    move: str = Field(description="招式")
    amount: int = Field(default=0, description="数量")

    def get_evo_i18n(self) -> str:
        move_obj = Move(condition="", name=self.move)
        return f"使用招式{move_obj.get_i18n_name()}{self.amount}次"


class WeatherRequirement(EvolutionRequirement):
    variant: Literal["weather"]

    isRaining: Optional[bool] = Field(default=None, description="是否下雨")
    isThundering: Optional[bool] = Field(default=None, description="是否雷雨")

    def get_evo_i18n(self) -> str:
        if self.isRaining is not None:
            return f"{'下雨' if self.isRaining else '不下雨'}"
        elif self.isThundering is not None:
            return f"{'雷雨' if self.isThundering else '不雷雨'}"
        else:
            return "未知"


class World(EvolutionRequirement):
    variant: Literal["world"]

    identifier: str = Field(description="世界标识符")

    def get_evo_i18n(self) -> str:
        return f"世界为{self.identifier}"


class BattleCriticalHits(EvolutionRequirement):
    variant: Literal["battle_critical_hits"]

    amount: int = Field(default=0, description="暴击次数")

    def get_evo_i18n(self) -> str:
        return f"战斗中暴击{self.amount}次"