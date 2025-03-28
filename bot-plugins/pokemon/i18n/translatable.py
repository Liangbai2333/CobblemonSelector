from abc import abstractmethod

from nonebot import logger

from plugins.pokemon.lang import get_lang


class Translatable:
    @abstractmethod
    def get_translation_key(self) -> str:
        pass

    def translate(self, value: str) -> str:
        return get_lang().get(f"cobblemon.{self.get_translation_key()}.{value}", value)

    def get_i18n_name(self) -> str:
        pass

    def get_i18n_desc(self) -> str:
        pass