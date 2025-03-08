from typing import Union, Optional, Any, Self

from pydantic import BaseModel, Field, model_validator, ModelWrapValidatorHandler

from plugins.pokemon.i18n.translatable import Translatable
from plugins.pokemon.lang import get_lang
from plugins.pokemon.loader.data import biome_map, feature_map


class BiomeValueRef(BaseModel):
    id: str = Field(description="id")
    required: bool = Field(description="是否必须")


class Biome(BaseModel, Translatable):
    translation_name: Optional[str] = Field(default=None, description="翻译名称")
    replace: bool = Field(description="替换")
    values: list[Union[str, BiomeValueRef]] = Field(description="值")


    @model_validator(mode="wrap")
    @classmethod
    def preprocess_data(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        if isinstance(data, str):
            if data in biome_map:
                return biome_map[data]
        return handler(data)

    def get_translation_key(self) -> str:
        return "worldgen.biome"

    def get_i18n_name(self) -> str:
        name = self.translation_name[1:] if self.translation_name.startswith("#") else self.translation_name
        if name.startswith("minecraft"):
            (namespace, key) = name.split(":")
            return get_lang().get(f"biome.{namespace}.{key}", name)
        elif name.startswith("cobblemon"):
            return self.translate(self.translation_name)
        else:
            return self.translate(self.translation_name)

    def __hash__(self):
        return hash(self.translation_name)