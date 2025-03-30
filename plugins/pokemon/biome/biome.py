from typing import Union, Optional, Any, Self

from pydantic import BaseModel, Field, model_validator, ModelWrapValidatorHandler, model_serializer
from pydantic_core.core_schema import SerializerFunctionWrapHandler

from plugins.pokemon.i18n.translatable import Translatable
from plugins.pokemon.lang import get_lang
from plugins.pokemon.loader.data import biome_map
from plugins.pokemon.spawn_pool.bucket import get_bucket, SpawnBucket
from plugins.pokemon.spawn_pool.detail import SpawnDetail


class BiomeValueRef(BaseModel):
    id: str = Field(description="id")
    required: bool = Field(description="是否必须")


class Biome(BaseModel, Translatable):
    translation_name: Optional[str] = Field(default=None, description="翻译名称")
    replace: bool = Field(description="替换")
    values: list[Union[str, BiomeValueRef]] = Field(description="值")

    details: Optional[list] = Field(default=None, description="生成详情", exclude=True)

    @model_serializer(mode="wrap")
    def serialize(self, nxt: SerializerFunctionWrapHandler):
        serialized = super().serialize(nxt)
        serialized["details"] = [{
            *detail,
            ""
        } for detail in self.get_non_repeat_pokemon_details()]
        serialized["search_name"] = self.get_search_name()
        serialized["image_url"] = self.get_image_url()
        serialized["pokedex_number"] = self.get_pokedex()
        return serialized


    @model_validator(mode="wrap")
    @classmethod
    def preprocess_data(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        if isinstance(data, str):
            if data in biome_map:
                return biome_map[data]
        return handler(data)

    def get_non_repeat_pokemon_details(self) -> list[SpawnDetail]:
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
            total = self.get_weight_account_for_bucket(bucket)
            percentage += (detail.weight / self.get_total_weight_for_bucket(bucket)) * total
            weight += detail.weight * total

        return percentage, weight


    def get_total_weight_for_bucket(self, bucket: SpawnBucket):
        return sum(map(lambda x: x.weight, filter(lambda x: x.bucket == bucket, self.details)))

    def get_weight_account_for_bucket(self, bucket: SpawnBucket):
        total = 0
        buckets = set()
        for detail in self.details:
            buckets.add(detail.bucket)

        for temp in buckets:
            total += temp.weight

        return bucket.weight / total


    def get_total_number_for_bucket_name(self, bucket_name: str):
        pokemon_temp = []
        count = 0
        for detail in self.details:
            if detail.bucket == get_bucket(bucket_name) and detail.pokemon not in pokemon_temp:
                count += 1
                pokemon_temp.append(detail.pokemon)

        return len(pokemon_temp)

    def get_total_weight(self):
        return sum(map(lambda x: x.weight * self.get_weight_account_for_bucket(x.bucket), self.details))

    def get_translation_key(self) -> str:
        return "worldgen.biome"

    def get_i18n_name(self) -> str:

        # name = self.translation_name[1:] if self.translation_name.startswith("#") else self.translation_name
        # name = name if name.startswith("minecraft") or name.startswith("aether") or name.startswith("cobblemon") else f"cobblemon:{name}"
        # name = f"#{name.replace(".", "/")}"
        return f"{self.__get_biome_i18n_name(self.translation_name)}"

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
            return get_lang().get(f"biome.{namespace}.{key}")
        elif name.startswith("cobblemon"):
            (_, key) = name.split(":")
            return self.translate(key)
        else:
            return self.translate(biome_name)


    def get_name_with_liked(self) -> str:
        name_original = self.translation_name
        if not name_original.startswith("#"):
            if not ":" in name_original:
                name_original = f"#cobblemon:{name_original.replace(".", "/")}"
            else:
                name_original = f"#{name_original.replace('.', '/')}"

        return name_original


    def __hash__(self):
        return hash(self.translation_name)