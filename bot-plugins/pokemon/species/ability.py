from typing import Any, Self

from pydantic import BaseModel, Field, model_validator

from plugins.pokemon.i18n.translatable import Translatable


class Ability(BaseModel, Translatable):
    prefix: str = Field(description="前缀")
    name: str = Field(description="能力名称")


    @model_validator(mode="before")
    @classmethod
    def preprocess_data(cls, data: Any) -> dict[str, Any]:
        if isinstance(data, str):
            if ":" in data:
                prefix, ability_name = data.split(":")
                return {"prefix": prefix.strip(), "name": ability_name.strip()}
            else:
                return {"prefix": "", "name": data.strip()}

        return data



    # @classmethod
    # def model_validate_json(
    #     cls,
    #     json_data: str | bytes | bytearray,
    #     *,
    #     strict: bool | None = None,
    #     context: Any | None = None,
    # ) -> Self:
    #     if isinstance(json_data, str):
    #         if ":" in json_data:
    #             prefix, ability_name = json_data.split(":")
    #             return cls(prefix=prefix, name=ability_name)
    #         else:
    #             return cls(prefix="", name=json_data)
    #
    #     return super().model_validate_json(json_data, strict=strict, context=context)


    def get_translation_key(self) -> str:
        return "ability"

    def get_i18n_name(self) -> str:
        return self.translate(self.name)

    def get_i18n_desc(self) -> str:
        return self.translate(f"{self.name}.desc")
