import json

from plugins.pokemon.path import resolve


class Lang(dict[str, str]):
    """
    语言文件映射
    """
    mapping: dict[str, str]

    def __init__(self, mapping: dict[str, str]):
        super().__init__()
        self.mapping = mapping

    def get(self, __key):
        return self.__getitem__(__key)

    def __getattr__(self, item: str):
        return self.mapping.get(item)

    def __getitem__(self, item: str):
        if item in self.mapping:
            return self.mapping[item]
        value = super().get(item)
        if value is not None:
            return value
        return item


mappings: dict[str, str] = json.load(open(resolve("lang/zh_cn.json"), "r", encoding="utf-8"))

lang = Lang(mapping=mappings)


def get_lang() -> Lang:
    """
    获取语言文件
    """
    return lang


def cobble_lang(key: str) -> str:
    return f"cobblemon.{key}"
