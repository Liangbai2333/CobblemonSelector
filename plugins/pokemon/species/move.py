from typing import Any, Union, Self, ClassVar

from pydantic import BaseModel, Field, model_validator, ModelWrapValidatorHandler

from plugins.pokemon.i18n.translatable import Translatable


class Move(BaseModel, Translatable):
    condition: Union[int, str] = Field(description="招式学习条件(等级或导师等等)")
    name: str = Field(description="招式名称")

    _registry: ClassVar[dict[str, Self]] = {}

    @model_validator(mode="wrap")
    @classmethod
    def preprocess_data(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        if isinstance(data, str):
            if data in cls._registry:
                return cls._registry[data]
            else:
                parts = data.split(":")
                if len(parts) == 1:
                    prefix = ""
                    move_name = parts[0]
                else:
                    prefix, move_name = parts

                if prefix.isdigit():
                    move =  Move(name=move_name, condition=int(prefix))
                else:
                    move = Move(name=move_name, condition=prefix)

                cls._registry[data] = move

                return move
        return handler(data)


    def is_level_move(self) -> bool:
        return isinstance(self.condition, int)


    def get_translation_key(self) -> str:
        return "move"

    def get_i18n_name(self) -> str:
        return self.translate(self.name)

    def get_i18n_desc(self) -> str:
        return self.translate(f"{self.name}.desc")
