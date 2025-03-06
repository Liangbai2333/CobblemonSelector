from enum import Enum
from typing import Literal, Optional

from pydantic import Field, field_validator, BaseModel

from plugins.pokemon.extension.type import TypedModel
from plugins.pokemon.species.feature import Feature


class EvolutionRequirement(TypedModel, type="variant"):
    variant: str = Field(description="进化需求选择器")


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


class AttackDefenceRatio(EvolutionRequirement):
    class AttackDefenceRatioEnum(Enum):
        ATTACK_HIGHER = "attack_higher"
        DEFENCE_HIGHER = "defence_higher"
        EQUAL = "equal"

    variant: Literal["attack_defence_ratio"]

    ratio: AttackDefenceRatioEnum = Field(description="比较")


class Biome(EvolutionRequirement):
    variant: Literal["biome"]

    biomeCondition: Optional[str] = Field(default=None, description="生物群系条件")
    biomeAnticondition: Optional[str] = Field(default=None, description="不匹配的生物群系条件")


class BlocksTraveledRequirement(EvolutionRequirement):
    variant: Literal["blocks_traveled"]

    amount: int = Field(default=0, description="移动距离")


class DamageTaken(EvolutionRequirement):
    variant: Literal["damage_taken"]

    amount: int = Field(default=0, description="伤害")


class Defeat(EvolutionRequirement):
    variant: Literal["defeat"]

    target: str = Field(description="目标")
    amount: int = Field(default=0, description="数量")


class Friendship(EvolutionRequirement):
    variant: Literal["friendship"]

    amount: int = Field(default=0, description="好感度")


class HeldItem(EvolutionRequirement):
    variant: Literal["held_item"]

    itemCondition: str = Field(description="道具")


class Level(EvolutionRequirement):
    variant: Literal["level"]

    minLevel: int = Field(default=1, description="最小等级")
    maxLevel: int = Field(default=100, description="最大等级")


class MoonPhase(EvolutionRequirement):
    variant: Literal["moon_phase"]

    moonPhase: str = Field(description="月相")


class MoveSet(EvolutionRequirement):
    variant: Literal["has_move"]

    move: str = Field(description="招式")


class MoveType(EvolutionRequirement):
    variant: Literal["has_move_type"]

    type: str = Field(description="招式类型")


class PartyMember(EvolutionRequirement):
    variant: Literal["party_member"]

    target: str = Field(description="目标")
    contains: bool = Field(default=True, description="是否包含")


class PlayerHasAdvancement(EvolutionRequirement):
    variant: Literal["advancement"]

    requiredAdvancement: str = Field(description="需求成就")


class PokemonProperties(EvolutionRequirement):
    variant: Literal["properties"]

    target: str = Field(description="目标")


class PropertyRange(EvolutionRequirement):
    variant: Literal["property_range"]

    range: tuple[int, int] = Field(description="范围")
    feature: Feature = Field(description="特性")


    @field_validator("range", mode="before")
    @classmethod
    def validate_range(cls, value: str) -> tuple[int, int]:
        splits = value.split("-")
        return int(splits[0]), int(splits[1])


class Recoil(EvolutionRequirement):
    variant: Literal["recoil"]

    amount: int = Field(default=0, description="反作用伤害")


class StatCompare(EvolutionRequirement):
    variant: Literal["stat_compare"]

    highStat: str = Field(description="高值")
    lowStat: str = Field(description="低值")


class StatEqual(EvolutionRequirement):
    variant: Literal["stat_equal"]

    statOne: str = Field(description="值1")
    statTwo: str = Field(description="值2")


class Structure(EvolutionRequirement):
    variant: Literal["structure"]

    structureCondition: Optional[str] = Field(default=None, description="结构条件")
    structureAnticondition: Optional[str] = Field(default=None, description="不匹配的结构条件")


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


class UseMove(EvolutionRequirement):
    variant: Literal["use_move"]

    move: str = Field(description="招式")
    amount: int = Field(default=0, description="数量")


class WeatherRequirement(EvolutionRequirement):
    variant: Literal["weather"]

    isRaining: Optional[bool] = Field(default=None, description="是否下雨")
    isThundering: Optional[bool] = Field(default=None, description="是否雷雨")


class World(EvolutionRequirement):
    variant: Literal["world"]

    identifier: str = Field(description="世界标识符")


class BattleCriticalHits(EvolutionRequirement):
    variant: Literal["battle_critical_hits"]

    amount: int = Field(default=0, description="暴击次数")