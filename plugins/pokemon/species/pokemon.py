from typing import Optional, TypeAlias, Any

from pydantic import BaseModel, Field, model_serializer

from plugins.pokemon.i18n.translatable import Translatable
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
    baseExperienceYield: Optional[int] = Field(default=None, description="Pokémon 经验值")
    moves: list[Move] = Field(default=[], description="Pokémon 招式")
    preEvolution: Optional[str] = Field(default=None, description="Pokémon 上一形态")
    evolutions: list[Evolution] = Field(default=[], description="Pokémon 进化")
    battleOnly: Optional[bool] = Field(default=None, description="是否 battleOnly")
    experienceGroup: Optional[str] = Field(default=None, description="Pokémon 经验值组")
    catchRate: Optional[int] = Field(default=None, description="Pokémon 捕捉率")
    eggCycles: Optional[int] = Field(default=None, description="Pokémon 蛋周期")
    baseFriendship: Optional[int] = Field(default=None, description="Pokémon 基础好感度")

    @model_serializer
    def serialize(self):
        serialized = {
            "species": self.species.name if self.species else None,
        }
        for field in self.model_fields.keys():
            if field in serialized:
                continue
            value = getattr(self, field, None)
            if value is not None:
                serialized[field] = value
        return serialized

    def get_translation_key(self) -> str:
        return "species"

    def get_i18n_name(self) -> str:
        return self.translate(f"{self.get_final_parent().get_name_lower_with_whitespace()}.name")

    def get_i18n_desc(self) -> str:
        return self.translate(f"{self.get_final_parent().get_name_lower_with_whitespace()}.desc")

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
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{self.nationalPokedexNumber}.png"

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


    # 报错因为装饰器吗？
    @model_serializer
    def serialize(self):
        serialized = {
            "implemented": self.implemented,
            "nationalPokedexNumber": self.nationalPokedexNumber,
            "features": self.features,
            # self.forms报错？
            "forms": [form.name for form in self.forms],
        }
        # 合并父类的序列化结果，仅保留非空字段
        # parent_serialized = super().serialize()
        # serialized.update({k: v for k, v in parent_serialized.items() if v is not None})
        for field in self.model_fields.keys():
            if field in serialized:
                continue
            value = getattr(self, field, None)
            if value is not None:
                serialized[field] = value
        return serialized

#
# def _resolve_pokemons_parent(pokemons: list[PokemonForm]):
#     """
#     为每个宝可梦形态设置其父宝可梦。
#
#     遍历宝可梦列表，对于每个宝可梦，再遍历其形态列表。
#     如果当前形态还有子形态，则递归调用本函数处理子形态。
#     最后，将当前形态的父宝可梦设置为当前宝可梦。
#
#     参数:
#     pokemons (list[PokemonForm]): 需要处理的宝可梦列表。
#     """
#     for pokemon in pokemons:
#         for form in pokemon.forms:
#             # 递归处理子形态
#             if form.forms:
#                 _resolve_pokemons_parent(form.forms)
#             # 设置当前形态的父宝可梦
#             form.parent = pokemon
#
#
# def _resolve_single_pokemon_evolution(mapping: dict[str, PokemonFromType], pokemon: PokemonFromType):
#     """
#     解析单个宝可梦的进化信息。
#
#     递归处理宝可梦的形式，以解析每个形式的进化信息。
#     如果宝可梦有进化链且尚未解析，则解析其进化条件。
#
#     :param mapping: 宝可梦名称到宝可梦对象的映射
#     :param pokemon: 需要解析进化的宝可梦对象
#     """
#     # 递归处理宝可梦的所有形式
#     if pokemon.forms:
#         for form in pokemon.forms:
#             _resolve_single_pokemon_evolution(mapping, form)
#
#     # 如果宝可梦有进化且尚未解析进化链，则进行解析
#     if pokemon.evolutions:
#         if pokemon.evolution_chain:
#             return
#
#         # 获取宝可梦的前一个进化形式
#         pre: str = pokemon.preEvolution
#         evolution_condition_list = []
#         for evolution in pokemon.evolutions:
#             # 获取进化结果的宝可梦名称
#             result: Optional[str] = evolution.get("result", None)
#             if not result:
#                 continue
#
#             # 获取进化所需的条件
#             requirements: list[dict[str, typing.Any]] = evolution.get("requirements", [])
#             if not requirements:
#                 continue
#
#             # 只处理单个要求的进化条件
#             if not requirements or len(requirements) > 1:
#                 continue
#
#             requirement = requirements[0]
#
#             # 根据进化条件的类型处理不同的进化要求
#             variant: str = requirement.get("variant", "")
#             if variant == "level":
#                 value = requirement["minLevel"]
#             elif variant == "friendship":
#                 value = requirement["amount"]
#             else:
#                 continue
#
#             # 获取进化结果的宝可梦对象
#             result_pokemon = mapping.get(result, None)
#             if not result_pokemon:
#                 continue
#
#             # 将解析的进化条件添加到列表中
#             evolution_condition_list.append(
#                 EvolutionCondition(
#                     evolution=result_pokemon,
#                     condition=variant,
#                     value=value
#                 )
#             )
#
#         # 构建并赋值宝可梦的进化链
#         pokemon.evolution_chain = EvolutionChain(
#             pre_evolution=mapping.get(pre, None),
#             evolution_conditions=evolution_condition_list
#         )
#
#
# def _resolve_pokemon_evolutions(mapping: dict[str, PokemonFromType]):
#     """
#     解析宝可梦的进化关系。
#
#     该函数遍历一个字典，字典的键是宝可梦的名称，值是宝可梦对象。
#     对于每个宝可梦对象，调用单个宝可梦进化解析函数，以建立或解析其进化关系。
#
#     参数:
#     - mapping: dict[str, PokemonFromType] | 包含宝可梦名称和宝可梦对象的字典。
#     """
#     # 遍历宝可梦字典，解析每个宝可梦的进化关系
#     for pokemon in mapping.values():
#         _resolve_single_pokemon_evolution(mapping, pokemon)
#
#
# __cache = {}
#
#
# def __get_name_to_forms(pokemon: PokemonForm) -> dict[str, PokemonForm]:
#     temp = {}
#     full_names = pokemon.get_names_lower_with_whitespace()
#     for full_name in full_names:
#         if full_name not in temp:
#             temp[full_name] = pokemon
#
#     return temp
#
#
# def _recursive_extract_forms(pokemon_dict: dict[str, Union[Pokemon, PokemonForm]]) -> dict[str, PokemonForm]:
#     """
#     递归地提取并合并宝可梦及其形态的信息。
#
#     本函数的目的是将给定的宝可梦字典中的每个宝可梦和它们的形态信息提取出来，
#     并合并到一个新的字典中。这包括递归地处理每个形态的名称与其对应的形态信息。
#
#     参数:
#     pokemon_dict: 一个字典，键为宝可梦的名称，值为宝可梦对象或宝可梦形态对象。
#
#     返回:
#     一个包含所有宝可梦及其形态信息的字典，键为名称，值为形态信息。
#     """
#     # 初始化一个临时字典来存储处理过程中的数据
#     temp = {}
#     # 将输入的字典复制到临时字典中，以避免直接修改原始字典
#     temp.update(pokemon_dict)
#     # 初始化另一个临时字典，用于存储递归处理的结果
#     temp2 = {}
#     # 遍历临时字典中的每个宝可梦对象
#     for pokemon in temp.values():
#         # 遍历每个宝可梦的形态列表
#         for form in pokemon.forms:
#             # 进行递归操作, 把所有符合要求的名字与form关联起来，并防止键值种类不对应的情况
#             temp2.update(_recursive_extract_forms(__get_name_to_forms(form)))
#
#     # 合并两个临时字典，得到最终的结果
#     temp.update(temp2)
#     # 返回合并后的字典
#     return temp


# def load_pokemons() -> dict[str, PokemonForm]:
#     """
#     加载并获取宝可梦列表
#     缓存未命中则尝试加载
#     :return: 宝可梦
#     """
#     if __cache:
#         return __cache
#
#     logger.info("Loading pokemons...")
#     path = resolve("species")
#     temp = {}
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             if not file.endswith(".json"):
#                 continue
#             with open(os.path.join(root, file), "r", encoding="utf-8") as f:
#                 temp[get_file_name_without_ext(file)] = Pokemon.model_validate_json(f.read())
#
#     pokemons = list(temp.values())
#     _resolve_pokemons_parent(pokemons)
#     count = len(pokemons)
#
#     for pokemon in pokemons:
#         name = pokemon.get_name_lower_with_whitespace()
#         if name not in temp:
#             temp[name] = pokemon
#
#     _resolve_pokemon_evolutions(_recursive_extract_forms(temp))
#     __cache.update(temp)
#
#     logger.info(f"Successfully loaded {count} Pokémon into cache")
#
#     return __cache
