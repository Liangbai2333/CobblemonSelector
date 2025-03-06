import itertools
import os

from nonebot import logger

from plugins.pokemon.biome.biome import Biome
from plugins.pokemon.loader.data import *
from plugins.pokemon.path import resolve, get_file_name_without_ext
from plugins.pokemon.selector.biome_detail import resolve_biome_to_details
from plugins.pokemon.spawn_pool.detail import SpawnDetail
from plugins.pokemon.spawn_pool.pool import SpawnPool
from plugins.pokemon.species.container import pokemon_container
from plugins.pokemon.species.feature import Feature
from plugins.pokemon.species.feature_attachment import FeatureAssignment
from plugins.pokemon.species.pokemon import Pokemon


def init_features():
    if feature_map:
        return feature_map
    logger.info("Loading features...")
    path = resolve("species_features")
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(".json"):
                continue
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                feature = Feature.model_validate_json(f.read())
                count += 1
                name = get_file_name_without_ext(file)
                feature_map[name] = feature
                for key in feature.keys:
                    feature_map[key] = feature
    logger.info(f"Successfully loaded {count} features into cache")
    return feature_map


def init_details() -> dict[str, list[SpawnDetail]]:
    if detail_map:
        return detail_map
    logger.info("Loading spawn pools...")
    path = resolve("spawn_pool")
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(".json"):
                continue
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                pool = SpawnPool.model_validate_json(f.read())
                details = pool.spawns
                for detail in details:
                    count += 1
                    detail.enabled = pool.enabled
                    if detail.pokemon not in detail_map:
                        detail_map[detail.pokemon] = [detail]
                    else:
                        detail_map[detail.pokemon].append(detail)
    logger.info(f"Successfully loaded {count} spawn pools into cache")
    return detail_map



def init_biomes() -> dict[str, Biome]:
    if biome_map:
        return biome_map

    logger.info("Loading biomes...")
    path = resolve("worldgen/biome")

    count = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(".json"):
                continue
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                biome = Biome.model_validate_json(f.read())
                name = get_file_name_without_ext(file)
                relpath = os.path.relpath(root, path)
                count += 1
                if relpath != ".":
                    translation_name = f"{relpath.replace('/', '.')}.{name}"
                    biome_map[f"{relpath.replace("/", ".")}.{name}"] = biome
                    biome_map[f"#cobblemon:{relpath}/{name}"] = biome
                else:
                    translation_name = name
                    biome_map[name] = biome
                    biome_map[f"#cobblemon:{name}"] = biome
                biome.translation_name = translation_name

    logger.info(f"Successfully loaded {count} biomes into cache")

    return biome_map



def init_pokemon_forms() -> dict[str, Biome]:
    if pokemon_container:
        return pokemon_container

    logger.info("Loading pokemon forms...")
    path = resolve("species")

    count = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(".json"):
                continue
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                pokemon = Pokemon.model_validate_json(f.read())
                name = get_file_name_without_ext(file)
                count += 1
                pokemon_container[pokemon.name.lower()] = pokemon
                pokemon_container[name] = pokemon

    logger.info(f"Successfully loaded {count} pokemon forms into cache")

    return pokemon_container


def _resolve_feature_assignments():
    logger.info("Resolving feature assignments...")
    path = resolve("species_feature_assignments")

    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(".json"):
                continue
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                assignment = FeatureAssignment.model_validate_json(f.read())
                for poke_name in assignment.pokemon:
                    if poke_name in pokemon_container:
                        pokemon_container[poke_name].features.extend(assignment.features)
                    else:
                        logger.warning(f"{poke_name} not found in pokemon_forms")

    logger.info("Successfully resolved feature assignments")


# 不要更改顺序
init_features()
init_biomes()
init_details()
init_pokemon_forms()
_resolve_feature_assignments()
logger.info("Resolving dependency relations...")
biome_to_details = resolve_biome_to_details(list(biome_map.values()), list(itertools.chain.from_iterable(detail_map.values())))
logger.info("Successfully resolved dependency relations")
