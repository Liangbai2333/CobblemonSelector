from typing import Any

from fastapi import APIRouter

spawn_router = APIRouter(
    prefix="/api/spawn",
    tags=["spawn"],
    responses={404: {"description": "Not found"}},
)

@spawn_router.get("/{name}")
async def get_spawns(name: str) -> list[dict[str, Any]] | dict[str, Any]:
    print(1)
    name = name.replace("$", " ")
    from plugins.pokemon import pokemon_container
    pokemon = pokemon_container.get(name)
    if pokemon is None:
        return {"error": "Pokemon not found"}
    return [spawn.model_dump() for spawn in pokemon.spawn_details]

@spawn_router.get("/{name}/{index}")
async def get_spawn(name: str, index: str) -> dict[str, Any]:
    name = name.replace("$", " ")
    from plugins.pokemon import pokemon_container
    pokemon = pokemon_container.get(name)
    if pokemon is None:
        return {"error": "Pokemon not found"}
    return pokemon.spawn_details[int(index)].model_dump()