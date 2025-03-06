from typing import TypeAlias, Any, Self, ClassVar

from pydantic import BaseModel, Field, model_validator, ModelWrapValidatorHandler

from plugins.pokemon.i18n.translatable import Translatable

class EggGroup(BaseModel, Translatable):
    name: str = Field(description="蛋组名称")

    _registry: ClassVar[dict[str, 'EggGroup']]

    @model_validator(mode="wrap")
    @classmethod
    def preprocess_data(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        if isinstance(data, str):
            return cls._registry[data]
        return handler(data)

    def get_translation_key(self) -> str:
        return "eggGroup"

    def get_i18n_name(self) -> str:
        return self.translate(self.name)


EggGroup._registry = {
        "monster": EggGroup(name="monster"),
        "water_1": EggGroup(name="water_1"),
        "bug": EggGroup(name="bug"),
        "flying": EggGroup(name="flying"),
        "field": EggGroup(name="field"),
        "fairy": EggGroup(name="fairy"),
        "grass": EggGroup(name="grass"),
        "human_like": EggGroup(name="human_like"),
        "water_3": EggGroup(name="water_3"),
        "mineral": EggGroup(name="mineral"),
        "amorphous": EggGroup(name="amorphous"),
        "water_2": EggGroup(name="water_2"),
        "ditto": EggGroup(name="ditto"),
        "dragon": EggGroup(name="dragon"),
        "undiscovered": EggGroup(name="undiscovered"),
    }