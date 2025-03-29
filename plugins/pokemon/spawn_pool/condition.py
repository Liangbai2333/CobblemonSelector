from typing import Optional

from pydantic import BaseModel, Field, field_validator, field_serializer, model_serializer
from pydantic_core.core_schema import SerializerFunctionWrapHandler

from plugins.pokemon.biome.biome import Biome
from plugins.pokemon.loader.data import biome_map


class SpawnCondition(BaseModel):
    biomes: list[Biome] = Field(default=[], description="生物群系")
    moonPhase: Optional[str | int] = Field(default=None, description="月相")
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

    def get_i18n_time_range(self):
        mapping = {
            "day": "白天",
            "night": "黑夜",
            "any": "任何时间",
            "dawn": "黎明",
            "dusk": "黄昏",
            "noon": "中午",
            "midnight": "午夜",
            "morning": "早上",
            "afternoon": "下午",
            "evening": "晚上"
        }
        return mapping.get(self.timeRange, self.timeRange)

    @model_serializer(mode="wrap")
    def serialize(self, nxt: SerializerFunctionWrapHandler):
        serialized = nxt(self)
        serialized["liked_biomes"] = [biome.get_name_with_liked() for biome in self.biomes]
        return serialized


    @field_validator("biomes", mode="before")
    @classmethod
    def validate_biomes(cls, value: list[str | Biome]) -> list[Biome]:
        temp = []
        biomes = biome_map
        for name in value:
            if isinstance(name, Biome):
                temp.append(name)
                continue
            if name in biomes:
                temp.append(biomes[name])
            else:
                biomes[name] = Biome(translation_name=name, replace=False, values=[name])
                temp.append(biomes[name])

        return temp