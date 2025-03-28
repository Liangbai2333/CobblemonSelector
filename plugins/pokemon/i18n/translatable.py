from abc import abstractmethod

from pydantic import model_serializer
from pydantic_core.core_schema import SerializerFunctionWrapHandler

from plugins.pokemon.lang import get_lang


class Translatable:

    @model_serializer(mode="wrap")
    def serialize(self, nxt: SerializerFunctionWrapHandler):
        serialized = nxt(self)
        serialized["i18n_name"] = self.get_i18n_name()
        desc = self.get_i18n_desc()
        if desc is not None:
            serialized["i18n_desc"] = desc
        return serialized


    @abstractmethod
    def get_translation_key(self) -> str:
        pass

    def translate(self, value: str) -> str:
        return get_lang().get(f"cobblemon.{self.get_translation_key()}.{value}")

    def get_i18n_name(self) -> str:
        pass

    def get_i18n_desc(self) -> str | None:
        return None