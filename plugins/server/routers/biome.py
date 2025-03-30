from typing import Any

from fastapi import APIRouter

from plugins.pokemon.biome.biome import Biome
from plugins.pokemon.loader.data import biome_map

biome_router = APIRouter(
    prefix="/api/biome",
    tags=["biome"],
    responses={404: {"description": "Not found"}},
)


@biome_router.get("/{name}")
async def get_biome(name: str) -> dict[str, Any]:
    biome: Biome = biome_map.get(name, None)
    if biome is None:
        return {"error": "Biome not found"}
    return biome.model_dump()