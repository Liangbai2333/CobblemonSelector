from typing import Union, Optional, Any

from pydantic import BaseModel, Field, model_validator

from plugins.pokemon.i18n.translatable import Translatable
from plugins.pokemon.loader.data import biome_map, feature_map


class BiomeValueRef(BaseModel):
    id: str = Field(description="id")
    required: bool = Field(description="是否必须")


class Biome(BaseModel, Translatable):
    translation_name: Optional[str] = Field(default=None, description="翻译名称")
    replace: bool = Field(description="替换")
    values: list[Union[str, BiomeValueRef]] = Field(description="值")


    @model_validator(mode="before")
    @classmethod
    def preprocess_data(cls, data: Any) -> dict[str, Any]:
        if isinstance(data, str):
            if data in biome_map:
                return feature_map[data]
        return data

    def get_translation_key(self) -> str:
        return "worldgen.biome"

    def get_i18n_name(self) -> str:
        return self.translate(self.translation_name)

    def __hash__(self):
        return hash(self.translation_name)