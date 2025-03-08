from typing import Union, Optional, Any, Self

from pydantic import BaseModel, Field, model_validator, ModelWrapValidatorHandler

from plugins.pokemon.i18n.translatable import Translatable
from plugins.pokemon.lang import get_lang
from plugins.pokemon.loader.data import biome_map
from plugins.pokemon.spawn_pool.bucket import get_bucket, SpawnBucket


class BiomeValueRef(BaseModel):
    id: str = Field(description="id")
    required: bool = Field(description="是否必须")


class Biome(BaseModel, Translatable):
    translation_name: Optional[str] = Field(default=None, description="翻译名称")
    replace: bool = Field(description="替换")
    values: list[Union[str, BiomeValueRef]] = Field(description="值")

    details: Optional[list] = Field(default=None, description="生成详情", exclude=True)


    @model_validator(mode="wrap")
    @classmethod
    def preprocess_data(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        if isinstance(data, str):
            if data in biome_map:
                return biome_map[data]
        return handler(data)

    def get_non_repeat_pokemon_details(self):
        pokemon_temp = []
        detail_temp = []
        for detail in self.details:
            if detail.pokemon not in pokemon_temp:
                detail_temp.append(detail)
                pokemon_temp.append(detail.pokemon)
        return detail_temp

    # 有四个桶 每个桶的概率都不一样
    def get_pokemon_spawn_percentage_and_weight(self, pokemon) -> (float, float):
        from plugins.pokemon.spawn_pool.detail import SpawnDetail
        details = filter(lambda x: x.get_pokemon_safely() == pokemon, self.details)
        percentage = 0
        weight = 0
        for detail in details:
            detail: SpawnDetail
            bucket = detail.bucket
            percentage += (detail.weight / self.get_total_weight_for_bucket(bucket)) * (bucket.weight / 100.0)
            weight += detail.weight * (bucket.weight / 100.0)

        return percentage, weight


    def get_total_weight_for_bucket(self, bucket: SpawnBucket):
        return sum(map(lambda x: x.weight, filter(lambda x: x.bucket == bucket, self.details)))


    def get_total_number_for_bucket_name(self, bucket_name: str):
        pokemon_temp = []
        count = 0
        for detail in self.details:
            if detail.bucket == get_bucket(bucket_name) and detail.pokemon not in pokemon_temp:
                count += 1
                pokemon_temp.append(detail.pokemon)
        return len(pokemon_temp)

    def get_total_weight(self):
        return sum(map(lambda x: x.weight * (x.bucket.weight / 100.0), self.details))

    def get_translation_key(self) -> str:
        return "worldgen.biome"

    def get_i18n_name(self) -> str:
        return self.__get_biome_i18n_name(self.translation_name)

    def get_sub_biomes_name(self) -> list[str]:
        temp = []
        for biome in self.values:
            if isinstance(biome, str):
                temp.append(self.__get_biome_i18n_name(biome))

        return temp

    def __get_biome_i18n_name(self, biome_name: str) -> str:
        name = biome_name[1:] if biome_name.startswith("#") else biome_name
        if name.startswith("minecraft"):
            (namespace, key) = name.split(":")
            return get_lang().get(f"biome.{namespace}.{key}", name)
        elif name.startswith("cobblemon"):
            (_, key) = name.split(":")
            return self.translate(key)
        else:
            return self.translate(biome_name)


    def __hash__(self):
        return hash(self.translation_name)