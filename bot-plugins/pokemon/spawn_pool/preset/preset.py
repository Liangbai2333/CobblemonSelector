from pydantic import BaseModel, Field

from plugins.pokemon.i18n.translatable import Translatable


class Preset(BaseModel, Translatable):
    name: str = Field(description="预设名称")

    def get_translation_key(self) -> str:
        return "preset"

    def get_i18n_name(self) -> str:
        return self.translate(self.name)