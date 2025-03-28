import os.path
from typing import Optional, TypeAlias, Any

from pydantic import BaseModel, Field, field_serializer, model_serializer
from pydantic_core.core_schema import SerializationInfo, SerializerFunctionWrapHandler

from plugins.pokemon.biome.biome import Biome
from plugins.pokemon.i18n.translatable import Translatable
from plugins.pokemon.lang import get_lang
from plugins.pokemon.spawn_pool.detail import SpawnDetail
from plugins.pokemon.species.ability import Ability
from plugins.pokemon.species.egg_group import EggGroup
from plugins.pokemon.species.evolution import Evolution
from plugins.pokemon.species.feature import Feature
from plugins.pokemon.species.move import Move

PokemonType: TypeAlias = 'Pokemon'
PokemonFromType: TypeAlias = 'PokemonForm'


class Stats(BaseModel):
    hp: int = Field(description="HP")
    attack: int = Field(description="攻击")
    defence: int = Field(description="防御")
    special_attack: int = Field(description="特攻")
    special_defence: int = Field(description="特防")
    speed: int = Field(description="速度")


def replace_whitespace_lower(text: str) -> str:
    return text.replace(" ", "").lower()


class PokemonForm(BaseModel, Translatable):
    species: PokemonType = Field(default=None, description="Pokémon 种类")
    original_name: Optional[str] = Field(default=None, description="Pokémon 文件原始名称")
    name: str = Field(description="Pokémon 名称")
    primaryType: str = Field(description="Pokémon 主类型")
    secondaryType: Optional[str] = Field(default=None, description="Pokémon 副类型")
    maleRatio: float = Field(description="Pokémon 性别比例")
    height: int = Field(description="Pokémon 高度")
    weight: int = Field(description="Pokémon 体重")
    pokedex: Optional[list[str]] = Field(default=None, description="Pokédex 描述")
    labels: Optional[list[str]] = Field(default=None, description="Pokémon 标签")
    abilities: Optional[list[Ability]] = Field(default=None, description="Pokémon 能力")
    eggGroups: Optional[list[EggGroup]] = Field(default=None, description="Pokémon 蛋组")
    aspects: list[str] = Field(default=[], description="Pokémon 方面")
    baseStats: Optional[Stats] = Field(default=None, description="Pokémon 种族值")
    baseExperienceYield: Optional[int] = Field(default=None, description="Pokémon 经验值产出")
    evYield: Optional[Stats] = Field(default=None, description="Pokémon 努力值产出")
    moves: list[Move] = Field(default=[], description="Pokémon 招式")
    preEvolution: Optional[str] = Field(default=None, description="Pokémon 上一形态")
    evolutions: list[Evolution] = Field(default=[], description="Pokémon 进化")
    battleOnly: Optional[bool] = Field(default=None, description="是否 battleOnly")
    experienceGroup: Optional[str] = Field(default=None, description="Pokémon 经验值组")
    catchRate: Optional[int] = Field(default=None, description="Pokémon 捕捉率")
    eggCycles: Optional[int] = Field(default=None, description="Pokémon 蛋周期")
    baseFriendship: Optional[int] = Field(default=None, description="Pokémon 基础好感度")

    biomes: Optional[list[Biome]] = Field(default=None, description="Pokémon  生成生物群系")
    spawn_details: Optional[list[SpawnDetail]] = Field(default=None, description="Pokémon 生成详情")

    @field_serializer("species")
    def serialize_species(self, species: PokemonType):
        return species.name if species else self.name


    @model_serializer(mode="wrap")
    def serialize(self, nxt: SerializerFunctionWrapHandler):
        serialized = super().serialize(nxt)
        serialized["search_name"] = self.get_search_name()
        serialized["image_url"] = self.get_image_url()
        serialized["pokedex_number"] = self.get_pokedex()
        return serialized

    # Failed: Recursive!!!
    # @model_serializer()
    # def serialize(self):
    #     serialized = self.model_dump(exclude={"species"})
    #     if self.species:
    #         serialized['species'] = self.species.name
    #     return serialized

    def get_hooked_name(self) -> str:
        return self.species.original_name if self.species else self.original_name

    def get_translation_key(self) -> str:
        return "species"

    def get_i18n_name(self) -> str:
        return self.translate(f"{self.get_hooked_name()}.name")

    def get_i18n_desc(self) -> str:
        return self.translate(f"{self.get_hooked_name()}.desc")

    def get_full_i18n_name(self) -> str:
        original = self.get_i18n_name()
        for aspect in self.aspects:
            aspect_key = f"cobblemon.form.aspect.{aspect}"
            if aspect_key in get_lang().mapping:
                original += get_lang().get(aspect_key)

        return original

    def get_spawn_biomes(self) -> list[Biome]:
        return self.biomes if self.biomes else []

    def get_pre_evolution_pokemon(self):
        from plugins.pokemon import container
        if self.preEvolution is None:
            return None
        return container.get(self.preEvolution, None)

    def get_full_name(self):
        return f"{self.species.name + "-" if self.species else ''}{self.name}"

    def get_search_name(self, split="_"):
        if not self.species:
            return f"{self.get_hooked_name()}"
        return f"{self.get_hooked_name()}{split}{split.join(self.aspects)}"

    def __hash__(self):
        return hash(f"{self.species.name if self.species else ""}{self.name}")

    def __getattribute__(self, item):
        try:
            # 尝试从当前对象获取属性
            value = super().__getattribute__(item)
            # 我们规定为none的属性从原始种类获取
            if value is None:
                raise AttributeError(f"{self.__class__.__name__} 对象没有属性 '{item}'")
            return value
        except AttributeError:
            # 获取parent属性（直接调用super避免递归）
            try:
                species = super().__getattribute__("species")
                if species is not None:
                    # 如果parent存在，从parent获取属性
                    return species.__getattribute__(item)
            except AttributeError:
                pass

            try:
                value = super().__getattribute__(item)
                if value is None:
                    return None
                else:
                    # 如果所有尝试都失败，抛出原始的AttributeError
                    raise AttributeError(f"{self.__class__.__name__} 对象没有属性 '{item}'")
            except AttributeError:
                raise AttributeError(f"{self.__class__.__name__} 对象没有属性 '{item}'")




    # def __getattribute__(self, item):
    #     value = super().__getattribute__(item)
    #     if value:
    #         return value
    #
    #     if item == "secondaryType":
    #         return value
    #
    #     if item == "evolutions" or item == "evolution_chain" or item == "preEvolution":
    #         return value
    #
    #     if item == "parent":
    #         return value
    #
    #     if self.parent:
    #         return self.parent.__getattribute__(item)
    #
    #     return value

    def get_image_url(self):
        return f"file://{os.path.join(os.getcwd(), f"images/{self.species.name if self.species else self.name}/{self.name}.png")}"

    def get_pokedex(self):
        """
        将数字转换为三位Pokédex格式
        参数:
            number: 整数，代表宝可梦的编号
        返回:
            字符串，三位数格式（如001, 022, 150, 1024）
        """
        number = self.nationalPokedexNumber
        if number < 10:
            # 个位数，在前面补两个0
            return f"00{number}"
        elif number < 100:
            # 两位数，在前面补一个0
            return f"0{number}"
        else:
            # 三位数及以上，保持原样
            return str(number)



class Pokemon(PokemonForm):
    implemented: bool = Field(default=False, description="是否已实现")
    nationalPokedexNumber: int = Field(description="Pokédex 编号")
    features: list[Feature] = Field(default=[], description="Pokémon 特性")
    forms: list[PokemonFromType] = Field(default=[], description="Pokémon 表现形态")

    def model_post_init(self, __context: Any) -> None:
        for form in self.forms:
            form.species = self

