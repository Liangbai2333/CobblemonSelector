from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from plugins.pokemon.spawn_pool.bucket import SpawnBucket, get_bucket
from plugins.pokemon.spawn_pool.condition import SpawnCondition
from plugins.pokemon.spawn_pool.preset.preset import Preset
from plugins.pokemon.spawn_pool.weight_multiplier import WeightMultiplier


class SpawnDetail(BaseModel):
    enabled: bool = Field(default=False, description="是否启用")
    pokemon: str = Field(description="Pokémon 名称")
    type: Literal["pokemon", "npc"] = Field(default="pokemon", description="生成类型")
    presets: list[Preset] = Field(default=[], description="预设")
    context: Literal[
        "grounded",
        "seafloor",
        "lavafloor",
        "submerged",
        "surface",
        "fishing"
    ] = Field(description="生成上下文")
    bucket: SpawnBucket = Field(description="桶")
    level: str = Field(description="等级")
    weight: float = Field(description="权重")
    condition: Optional[SpawnCondition] = Field(default=None, description="生成条件")
    anticondition: Optional[SpawnCondition] = Field(default=None, description="生成条件非")
    weightMultiplier: Optional[WeightMultiplier] = Field(default=None, description="权重倍率")
    percentage: Optional[float] = Field(default=None, description="百分比")
    labels: list[str] = Field(default=[], description="标签")


    def is_regional(self) -> bool:
        return len(self.pokemon.split(" ")) > 1

    def get_pokemon_safely(self):
        from plugins.pokemon import container
        return container.get(self.pokemon, None)

    def get_pokemon(self):
        from plugins.pokemon import container
        return container[self.pokemon]


    @field_validator("bucket", mode="before")
    @classmethod
    def validate_bucket(cls, value: str | SpawnBucket) -> SpawnBucket:
        if isinstance(value, SpawnBucket):
            return value
        return get_bucket(value)

    @field_validator("presets", mode="before")
    @classmethod
    def validate_presets(cls, value: list[str | Preset]) -> list[Preset]:
        return [Preset(name=preset) if isinstance(preset, str) else preset for preset in value]