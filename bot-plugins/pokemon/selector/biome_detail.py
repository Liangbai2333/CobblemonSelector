from plugins.pokemon import pokemon_container
from plugins.pokemon.biome.biome import Biome
from plugins.pokemon.spawn_pool.detail import SpawnDetail


def resolve_biome_to_details(biomes: list[Biome], details: list[SpawnDetail]):
    """
    将生物群系映射到详细的生成信息。

    此函数接受两个列表作为输入：生物群系列表和生成详情列表。
    它会将每个生物群系与其相关的生成详情列表进行匹配，并返回一个字典，
    其中每个生物群系都是键，对应的生成详情列表为值。

    参数:
    biomes (list[Biome]): 生物群系的列表。
    details (list[SpawnDetail]): 生成详情的列表，每个详情都包含有关在特定生物群系中生成的信息。
    """

    # 遍历生物群系列表
    for biome in biomes:
        # 初始化当前生物群系的生成详情列表
        biome_details = []

        # 遍历生成详情列表
        for detail in details:
            # 如果生成详情适用于当前生物群系
            if detail.condition and biome in detail.condition.biomes:
                # 将生成详情添加到当前生物群系的详情列表中
                if detail not in biome_details:
                    biome_details.append(detail)
        # 将生物群系及其对应的生成详情列表添加到字典中
        biome.details = biome_details


def resolve_reversed_pokemon_to_biomes(biomes: list[Biome], details: list[SpawnDetail]):
    """
    将生物群系映射到详细的生成信息。
    """

    for detail in details:
        try:
            pokemon = pokemon_container[detail.pokemon]
        except KeyError:
            continue
        # 如果生成详情适用于当前生物群系
        if not pokemon.spawn_details:
            pokemon.spawn_details = [detail]
        else:
            if detail not in pokemon.spawn_details:
                pokemon.spawn_details.append(detail)

        for biome in biomes:
            if detail.condition and biome in detail.condition.biomes:
                # 将生成详情添加到当前生物群系的详情列表中
                if not pokemon.biomes:
                    pokemon.biomes = [biome]
                else:
                    if biome not in pokemon.biomes:
                        pokemon.biomes.append(biome)

