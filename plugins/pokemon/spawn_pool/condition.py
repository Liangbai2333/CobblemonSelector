from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator

from plugins.pokemon.biome.biome import Biome
from plugins.pokemon.loader.data import biome_map


class SpawnCondition(BaseModel):
    biomes: list[Biome] = Field(default=[], description="生物群系")
    moonPhase: list[str] = Field(default=[], description="月相")
    canSeeSky: Optional[bool] = Field(default=None, description="是否能看见天空")
    minX: Optional[float] = Field(default=None, description="X轴最小值")
    minY: Optional[float] = Field(default=None, description="Y轴最小值")
    minZ: Optional[float] = Field(default=None, description="Z轴最小值")
    maxX: Optional[float] = Field(default=None, description="X轴最大值")
    maxY: Optional[float] = Field(default=None, description="Y轴最大值")
    maxZ: Optional[float] = Field(default=None, description="Z轴最大值")
    minLight: Optional[int] = Field(default=None, description="最小光照值")
    maxLight: Optional[int] = Field(default=None, description="最大光照值")
    minSkyLight: Optional[int] = Field(default=None, description="最小天空光照值")
    maxSkyLight: Optional[int] = Field(default=None, description="最大天空光照值")
    isRaining: Optional[bool] = Field(default=None, description="是否下雨")
    isThundering: Optional[bool] = Field(default=None, description="是否雷雨")
    timeRange: Optional[str] = Field(default=None, description="时间范围")
    isSlimeChunk: Optional[bool] = Field(default=None, description="是否是史莱姆区块")


    @field_validator("biomes", mode="before")
    @classmethod
    def validate_biomes(cls, value: list[str]) -> list[Biome]:
        temp = []
        biomes = biome_map
        for name in value:
            if name in biomes:
                temp.append(biomes[name])
            else:
                biomes[name] = Biome(translation_name=name, replace=False, values=[name])
                temp.append(biomes[name])

        return temp

    @field_validator("moonPhase", mode="before")
    @classmethod
    def validate_moon_phase(cls, value: Union[str, int]) -> list[str]:
        temp = []

        if isinstance(value, int):
            temp.append(str(value))
        else:
            temp.extend(value.split(","))

        # 定义月相范围映射
        moon_phase_ranges = {
            "crescent": {3, 5},
            "gibbous": {1, 7},
            "full": {0},
            "new": {4},
            "quarter": {2, 6},
            "waxing": {5, 7},
            "waning": {1, 3},
        }

        # 将数字映射到月相名称
        result = []
        for num_str in temp:
            if not num_str.isdigit():
                raise ValueError(f"Invalid moon phase number: {num_str}")

            num = int(num_str)
            matched_phases = [
                phase for phase, numbers in moon_phase_ranges.items() if num in numbers
            ]

            if not matched_phases:
                raise ValueError(f"No matching moon phase for number: {num}")

            result.extend(matched_phases)

        return result