import json
from typing import Optional

from pydantic import Field, BaseModel

from plugins.pokemon.path import resolve

class Lang(BaseModel):
    """
    语言文件映射
    """
    mapping: dict[str, str] = Field(description="语言文件映射")

    def __getattr__(self, item: str):
        return self.mapping.get(item)

    def get(self, item: str, default: Optional[str] = None):
        return self.mapping.get(item, default)


mappings: dict[str, str] = json.load(open(resolve("lang/zh_cn.json"), "r", encoding="utf-8"))

lang = Lang(mapping=mappings)

def get_lang() -> Lang:
    """
    获取语言文件
    """
    return lang

