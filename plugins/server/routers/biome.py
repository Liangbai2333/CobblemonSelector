from typing import Any

from fastapi import APIRouter

from plugins.pokemon.biome.biome import Biome
from plugins.pokemon.loader.data import biome_map
from plugins.pokemon.spawn_pool.bucket import get_buckets

biome_router = APIRouter(
    prefix="/api/biome",
    tags=["biome"],
    responses={404: {"description": "Not found"}},
)


@biome_router.get("/{name}")
async def get_biome(name: str) -> dict[str, Any]:
    from plugins.pokemon.spawn_pool.detail import SpawnDetail

    biome: Biome = biome_map.get(name, None)
    if biome is None:
        return {"error": "Biome not found"}

    serialized = biome.model_dump()

    details = []
    for detail in biome.get_non_repeat_pokemon_details():
        detail: SpawnDetail
        pokemon = detail.get_pokemon_safely()
        if pokemon is None:
            continue
        percentage, weight = biome.get_pokemon_spawn_percentage_and_weight(pokemon)
        details.append({
            "enabled": detail.enabled,
            "target": pokemon.get_i18n_name(),
            "imageUrl": pokemon.get_image_url(),
            "levelRange": detail.level,
            "bucket": detail.bucket,
            "percentage": percentage,
            "weight": weight,
        })

    serialized["details"] = details
    buckets = []
    for bucket in get_buckets():
        buckets.append({
            **bucket.model_dump(),
            "num_pokemon": biome.get_total_number_for_bucket_name(bucket.name),
            "total_weight": biome.get_total_weight_for_bucket(bucket),
        })

    serialized["buckets"] = buckets
    serialized["total_weight"] = biome.get_total_weight()
    serialized["sub_biomes"] = biome.get_sub_biomes_name()
    return serialized